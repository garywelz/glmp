# Read-only replay: predict dna_topology_class after has_not/has_and fix.
$ErrorActionPreference = "Stop"
$Q = 0.05
$CustomPwm = @("LacI_lacO1", "TrpR_trpO", "LexA_SOS_box")

function Site-PassesThreshold($site) {
    $mid = $site.motif_id
    if ($CustomPwm -contains $mid) { return [double]$site.pvalue -le $Q }
    return [double]$site.qvalue -le $Q
}

function Get-RepressorSite($rel, $siteMap) {
    $a = $siteMap[$rel.site_a_key]
    $b = $siteMap[$rel.site_b_key]
    if ($a.is_repressor) { return $a }
    if ($b.is_repressor) { return $b }
    return $null
}

function Rel-InvolvesKnownTf($rel, $siteMap) {
    $a = $siteMap[$rel.site_a_key]
    $b = $siteMap[$rel.site_b_key]
    return ($a.is_repressor -or $a.is_activator -or $b.is_repressor -or $b.is_activator)
}

function Rel-Eligible($rel, $siteMap) {
    if (-not (Rel-InvolvesKnownTf $rel $siteMap)) { return $false }
    if ($rel.logic_type -eq "NOT") {
        $rep = Get-RepressorSite $rel $siteMap
        if ($rep -and -not (Site-PassesThreshold $rep)) { return $false }
    }
    return $true
}

function Rel-Confident($rel, $siteMap) {
    $a = $siteMap[$rel.site_a_key]
    $b = $siteMap[$rel.site_b_key]
    if ($rel.logic_type -eq "NOT") {
        $rep = Get-RepressorSite $rel $siteMap
        if ($rep) { return (Site-PassesThreshold $rep) }
        return ((Site-PassesThreshold $a) -and (Site-PassesThreshold $b))
    }
    if ($rel.logic_type -eq "AND") {
        $known = @($a, $b) | Where-Object { $_.is_repressor -or $_.is_activator }
        if ($known.Count -gt 0) {
            foreach ($s in $known) { if (-not (Site-PassesThreshold $s)) { return $false } }
            return $true
        }
    }
    return ((Site-PassesThreshold $a) -and (Site-PassesThreshold $b))
}

function Proposed-Class($hasNot, $hasAnd) {
    if ($hasNot -and $hasAnd) { return "II", @("NOT", "AND") }
    if ($hasNot) { return "I/II", @("NOT") }
    if ($hasAnd) { return "I", @("AND") }
    return $null, @()
}

function Assess-Classification($rels, $hasNot, $hasAnd, $organism) {
    $proposed, $supportTypes = Proposed-Class $hasNot $hasAnd
    $stats = @{
        proposed_class = $proposed
        supporting_gate_types = $supportTypes
        supporting_gates_total = 0
        supporting_gates_confident = 0
        supporting_gates_weak = 0
    }
    if (-not $proposed) { return "INDETERMINATE", $null, "insufficient", $stats }

    $supporting = $rels | Where-Object {
        ($supportTypes -contains $_.logic_type) -and (Rel-Eligible $_ $_.siteMap)
    }
    $stats.supporting_gates_total = @($supporting).Count
    if ($stats.supporting_gates_total -eq 0) {
        return "INSUFFICIENT_EVIDENCE", "No supporting gates", "insufficient", $stats
    }

    $confident = @($supporting | Where-Object { Rel-Confident $_ $_.siteMap })
    $weak = $stats.supporting_gates_total - $confident.Count
    $stats.supporting_gates_confident = $confident.Count
    $stats.supporting_gates_weak = $weak

    $geomWarn = ($organism -eq "s_cerevisiae") -or ($organism -eq "phage_lambda")
    if ($geomWarn -and ($proposed -in @("II", "III", "IV", "V"))) {
        $confNot = @($confident | Where-Object { $_.logic_type -eq "NOT" })
        if ($confNot.Count -eq 0) {
            return "INSUFFICIENT_EVIDENCE", "geometry weak", "insufficient", $stats
        }
    }
    if ($weak -gt $confident.Count) {
        return "INSUFFICIENT_EVIDENCE", "weak majority", "insufficient", $stats
    }
    $topoConf = if ($confident.Count -ge 2) { "high" } elseif ($confident.Count -ge 1) { "medium" } else { "partial" }
    if ($geomWarn) { $topoConf = "partial" }
    return $proposed, $null, $topoConf, $stats
}

function Load-And-Predict($path) {
    $data = Get-Content $path -Raw | ConvertFrom-Json
    $siteMap = @{}
    foreach ($s in $data.binding_sites) {
        $key = "$($s.motif_id)|$($s.start)-$($s.stop)"
        $siteMap[$key] = $s
    }
    $rels = @()
    foreach ($r in $data.relationships) {
        $posA = ($r.site_a_pos -replace "\u2013", "-")
        $posB = ($r.site_b_pos -replace "\u2013", "-")
        $obj = [PSCustomObject]@{
            logic_type = $r.logic_type
            site_a_key = "$($r.site_a)|$posA"
            site_b_key = "$($r.site_b)|$posB"
            siteMap = $siteMap
        }
        $rels += $obj
    }

    $rawNot = ($rels.logic_type -contains "NOT")
    $rawAnd = ($rels.logic_type -contains "AND")
    $eligible = @($rels | Where-Object { Rel-Eligible $_ $siteMap })
    $fixNot = @($eligible | Where-Object { $_.logic_type -eq "NOT" }).Count -gt 0
    $fixAnd = @($eligible | Where-Object { $_.logic_type -eq "AND" }).Count -gt 0
    $eNot = @($eligible | Where-Object { $_.logic_type -eq "NOT" }).Count
    $eAnd = @($eligible | Where-Object { $_.logic_type -eq "AND" }).Count

    $cur = $data.dna_topology_class
    $newCls, $note, $conf, $stats = Assess-Classification $rels $fixNot $fixAnd $data.organism

    [PSCustomObject]@{
        circuit = $data.circuit_name
        file = Split-Path $path -Leaf
        current_class = $cur
        current_bio = $data.glmp_biological_class
        raw_has_not = $rawNot
        raw_has_and = $rawAnd
        fix_has_not = $fixNot
        fix_has_and = $fixAnd
        eligible_not = $eNot
        eligible_and = $eAnd
        predicted_class = $newCls
        predicted_conf = $conf
        flip = ($newCls -ne $cur)
        support_total = $stats.supporting_gates_total
        support_conf = $stats.supporting_gates_confident
    }
}

$results = Join-Path (Split-Path $PSScriptRoot -Parent) "results"
$files = @(
    "lac_operon_logic_v2.json",
    "ara_operon_logic_v3.json",
    "trp_operon_logic_v4.json",
    "ecoli_sos_lexa_logic_20260702.json",
    "ecoli_sos_reca_logic_20260702.json",
    "ecoli_flhdc_flagellar_logic_20260701.json",
    "ecoli_lambda_switch_logic_20260703.json",
    "ecoli_dna_damage_checkpoint_logic_20260705.json"
)

$rows = foreach ($f in $files) {
    Load-And-Predict (Join-Path $results $f)
}
$rows | ConvertTo-Csv -NoTypeInformation | Write-Output
Write-Host "`nClass II after fix: $(@($rows | Where-Object { $_.predicted_class -eq 'II' }).Count) circuits"
Write-Host "Flips: $(@($rows | Where-Object { $_.flip }).Count) circuits"
