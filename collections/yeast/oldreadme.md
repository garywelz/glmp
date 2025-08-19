
<!doctype html>
<html class="">
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
		<meta name="description" content="This application helps users model biological processes, such as those in yeast and E. coli, as computational programs. Users can explore detailed diagrams and logic patterns of cellular processes,..." />
		<meta property="fb:app_id" content="1321688464574422" />
		<meta name="twitter:card" content="summary_large_image" />
		<meta name="twitter:site" content="@huggingface" />
		<meta name="twitter:image" content="https://cdn-thumbnails.huggingface.co/social-thumbnails/spaces/garywelz/glmp.png" />
		<meta property="og:title" content="Genome Logic Modeling Project (GLMP) - a Hugging Face Space by garywelz" />
		<meta property="og:type" content="website" />
		<meta property="og:url" content="https://huggingface.co/spaces/garywelz/glmp" />
		<meta property="og:image" content="https://cdn-thumbnails.huggingface.co/social-thumbnails/spaces/garywelz/glmp.png" />

		<link rel="stylesheet" href="/front/build/kube-838da81/style.css" />

		<link rel="preconnect" href="https://fonts.gstatic.com" />
		<link
			href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;1,200;1,300;1,400;1,600;1,700&display=swap"
			rel="stylesheet"
		/>
		<link
			href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&display=swap"
			rel="stylesheet"
		/>

		<link
			rel="preload"
			href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.12.0/katex.min.css"
			as="style"
			onload="this.onload=null;this.rel='stylesheet'"
		/>
		<noscript>
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.12.0/katex.min.css" />
		</noscript>

		<script>const guestTheme = document.cookie.match(/theme=(\w+)/)?.[1]; document.documentElement.classList.toggle('dark', guestTheme === 'dark' || ( (!guestTheme || guestTheme === 'system') && window.matchMedia('(prefers-color-scheme: dark)').matches));</script>
<link rel="canonical" href="https://huggingface.co/spaces/garywelz/glmp"> <script type="application/ld+json">{
  "@context": "https:\/\/schema.org",
  "@type": "WebApplication",
  "name": "Genome Logic Modeling Project (GLMP)",
  "identifier": "garywelz\/glmp",
  "creator": {
    "@type": "Person",
    "name": "Gary Welz",
    "url": "https:\/\/huggingface.co\/garywelz"
  },
  "applicationCategory": "AIApplication",
  "sameAs": "garywelz-glmp",
  "url": "https:\/\/huggingface.co\/spaces\/garywelz\/glmp",
  "operatingSystem": "Web"
}</script> 

		<title>Genome Logic Modeling Project (GLMP) - a Hugging Face Space by garywelz</title>

		<script
			defer
			data-domain="huggingface.co"
			event-loggedIn="true"
			src="/js/script.pageview-props.js"
		></script>
		<script>
			window.plausible =
				window.plausible ||
				function () {
					(window.plausible.q = window.plausible.q || []).push(arguments);
				};
		</script>
		<script>
			window.hubConfig = {"features":{"signupDisabled":false},"sshGitUrl":"git@hf.co","moonHttpUrl":"https:\/\/huggingface.co","captchaApiKey":"bd5f2066-93dc-4bdd-a64b-a24646ca3859","captchaDisabledOnSignup":true,"datasetViewerPublicUrl":"https:\/\/datasets-server.huggingface.co","stripePublicKey":"pk_live_x2tdjFXBCvXo2FFmMybezpeM00J6gPCAAc","environment":"production","userAgent":"HuggingFace (production)","spacesIframeDomain":"hf.space","spacesApiUrl":"https:\/\/api.hf.space","docSearchKey":"ece5e02e57300e17d152c08056145326e90c4bff3dd07d7d1ae40cf1c8d39cb6","logoDev":{"apiUrl":"https:\/\/img.logo.dev\/","apiKey":"pk_UHS2HZOeRnaSOdDp7jbd5w"}};
		</script>
		<script type="text/javascript" src="https://de5282c3ca0c.edge.sdk.awswaf.com/de5282c3ca0c/526cf06acb0d/challenge.js" defer></script> 
	</head>
	<body class="flex flex-col min-h-dvh bg-white dark:bg-gray-950 text-black SpacePage">
		<div class="flex min-h-dvh flex-col"><div class="SVELTE_HYDRATER contents" data-target="SystemThemeMonitor" data-props="{&quot;isLoggedIn&quot;:true}"></div>

	
	<div class="SVELTE_HYDRATER contents" data-target="SpaceHeader" data-props="{&quot;activeTab&quot;:&quot;spaceApp&quot;,&quot;authLight&quot;:{&quot;csrfToken&quot;:&quot;eyJkYXRhIjp7ImV4cGlyYXRpb24iOjE3NTU2MjQyODExMDUsInVzZXJJZCI6IjY3Yzc1Y2RkMmU1NDdhMTIzMDk4YjA5MSJ9LCJzaWduYXR1cmUiOiIyMzZmODk3MDNjOTA3NmY3MTY3OTg5NDIwZTRmNTUzNmE0MGNkYjk1OGVlNTFmNWYzMWIwYWVkOGYyZjA4YTJkIn0=&quot;,&quot;hasHfLevelAccess&quot;:false,&quot;u&quot;:{&quot;avatarUrl&quot;:&quot;https://cdn-avatars.huggingface.co/v1/production/uploads/67c75cdd2e547a123098b091/Z0x0RIn4jBulG2IgNVx8J.jpeg&quot;,&quot;isPro&quot;:false,&quot;orgs&quot;:[],&quot;user&quot;:&quot;garywelz&quot;,&quot;canPost&quot;:false,&quot;canHaveBilling&quot;:true,&quot;canCreateOrg&quot;:true,&quot;theme&quot;:&quot;light&quot;,&quot;notifications&quot;:{&quot;org_suggestions&quot;:false},&quot;hardwareItems&quot;:[],&quot;hardwareItemsPrivate&quot;:false,&quot;usage&quot;:{&quot;storage&quot;:{&quot;used&quot;:52107958,&quot;usedPrivate&quot;:0,&quot;usedPublic&quot;:52107958,&quot;count&quot;:2,&quot;limit&quot;:100000000000,&quot;summary&quot;:{&quot;space&quot;:{&quot;used&quot;:52107958,&quot;usedPrivate&quot;:0,&quot;usedPublic&quot;:52107958,&quot;count&quot;:2}}},&quot;inference&quot;:{&quot;usedNanoUsd&quot;:0,&quot;numRequests&quot;:0,&quot;providerDetails&quot;:[],&quot;periodEnd&quot;:&quot;2025-08-31T23:59:59.999Z&quot;,&quot;periodStart&quot;:&quot;2025-08-01T00:00:00.000Z&quot;,&quot;includedNanoUsd&quot;:100000000,&quot;limitNanoUsd&quot;:100000000,&quot;lastUpdated&quot;:&quot;2025-08-18T17:24:20.798Z&quot;},&quot;zeroGpu&quot;:{&quot;base&quot;:210,&quot;current&quot;:210,&quot;lastUpdated&quot;:&quot;2025-08-18T17:24:20.798Z&quot;}},&quot;welcomeLinks&quot;:[]}},&quot;author&quot;:{&quot;_id&quot;:&quot;67c75cdd2e547a123098b091&quot;,&quot;avatarUrl&quot;:&quot;https://cdn-avatars.huggingface.co/v1/production/uploads/67c75cdd2e547a123098b091/Z0x0RIn4jBulG2IgNVx8J.jpeg&quot;,&quot;fullname&quot;:&quot;Gary Welz&quot;,&quot;name&quot;:&quot;garywelz&quot;,&quot;type&quot;:&quot;user&quot;,&quot;isPro&quot;:false,&quot;isHf&quot;:false,&quot;isHfAdmin&quot;:false,&quot;isMod&quot;:false,&quot;isUserFollowing&quot;:false},&quot;avatarUrl&quot;:&quot;https://cdn-avatars.huggingface.co/v1/production/uploads/67c75cdd2e547a123098b091/Z0x0RIn4jBulG2IgNVx8J.jpeg&quot;,&quot;canDisable&quot;:false,&quot;canReadRepoSettings&quot;:true,&quot;canWriteRepoSettings&quot;:true,&quot;canWrite&quot;:true,&quot;discussionsStats&quot;:{&quot;closed&quot;:0,&quot;open&quot;:0,&quot;total&quot;:0},&quot;query&quot;:{},&quot;space&quot;:{&quot;author&quot;:&quot;garywelz&quot;,&quot;colorFrom&quot;:&quot;blue&quot;,&quot;colorTo&quot;:&quot;green&quot;,&quot;cardData&quot;:{&quot;title&quot;:&quot;Genome Logic Modeling Project (GLMP)&quot;,&quot;emoji&quot;:&quot;🧬&quot;,&quot;colorFrom&quot;:&quot;blue&quot;,&quot;colorTo&quot;:&quot;green&quot;,&quot;sdk&quot;:&quot;static&quot;,&quot;sdk_version&quot;:&quot;latest&quot;,&quot;app_file&quot;:&quot;README.md&quot;,&quot;pinned&quot;:false},&quot;createdAt&quot;:&quot;2025-07-28T19:47:08.000Z&quot;,&quot;emoji&quot;:&quot;🧬&quot;,&quot;discussionsDisabled&quot;:false,&quot;duplicationDisabled&quot;:false,&quot;id&quot;:&quot;garywelz/glmp&quot;,&quot;isLikedByUser&quot;:true,&quot;watched&quot;:{&quot;isWatching&quot;:true,&quot;isMuted&quot;:false,&quot;mode&quot;:&quot;global&quot;},&quot;lastModified&quot;:&quot;2025-08-18T16:35:58.000Z&quot;,&quot;likes&quot;:1,&quot;pinned&quot;:false,&quot;private&quot;:false,&quot;gated&quot;:false,&quot;repoType&quot;:&quot;space&quot;,&quot;subdomain&quot;:&quot;garywelz-glmp&quot;,&quot;sdk&quot;:&quot;static&quot;,&quot;sdkVersion&quot;:&quot;latest&quot;,&quot;staticOrigin&quot;:&quot;README.md&quot;,&quot;title&quot;:&quot;Genome Logic Modeling Project (GLMP)&quot;,&quot;runtime&quot;:{&quot;stage&quot;:&quot;RUNNING&quot;,&quot;hardware&quot;:{&quot;current&quot;:null,&quot;requested&quot;:null},&quot;storage&quot;:null,&quot;replicas&quot;:{&quot;requested&quot;:1,&quot;current&quot;:1}},&quot;iframe&quot;:{&quot;embedSrc&quot;:&quot;https://garywelz-glmp.static.hf.space&quot;,&quot;src&quot;:&quot;https://garywelz-glmp.static.hf.space/README.md&quot;},&quot;secrets&quot;:[],&quot;variables&quot;:[],&quot;linkedModels&quot;:[],&quot;linkedDatasets&quot;:[],&quot;linkedCollections&quot;:[],&quot;sha&quot;:&quot;b8ec5961c9d22b5b3b686d476c495e92c45b7864&quot;,&quot;hasBlockedOids&quot;:false,&quot;region&quot;:&quot;us&quot;,&quot;tags&quot;:[&quot;static&quot;,&quot;region:us&quot;],&quot;xetEnabled&quot;:false},&quot;u&quot;:{&quot;avatarUrl&quot;:&quot;https://cdn-avatars.huggingface.co/v1/production/uploads/67c75cdd2e547a123098b091/Z0x0RIn4jBulG2IgNVx8J.jpeg&quot;,&quot;isPro&quot;:false,&quot;fullname&quot;:&quot;Gary Welz&quot;,&quot;user&quot;:&quot;garywelz&quot;,&quot;orgs&quot;:[],&quot;signup&quot;:{&quot;github&quot;:&quot;garywelz&quot;,&quot;twitter&quot;:&quot;garywelz&quot;,&quot;details&quot;:&quot;Creating knowledge agents&quot;},&quot;isHf&quot;:false,&quot;isMod&quot;:false,&quot;type&quot;:&quot;user&quot;,&quot;theme&quot;:&quot;light&quot;,&quot;canPay&quot;:false,&quot;spacesAvailableFlavors&quot;:[&quot;cpu-basic&quot;,&quot;cpu-upgrade&quot;,&quot;zero-a10g&quot;,&quot;t4-small&quot;,&quot;t4-medium&quot;,&quot;l4x1&quot;,&quot;l4x4&quot;,&quot;l40sx1&quot;,&quot;l40sx4&quot;,&quot;l40sx8&quot;,&quot;a10g-small&quot;,&quot;a10g-large&quot;,&quot;a10g-largex2&quot;,&quot;a10g-largex4&quot;,&quot;a100-large&quot;],&quot;canPost&quot;:false},&quot;unreadNotifications&quot;:0,&quot;unreadChangelogCount&quot;:3,&quot;sessionUuid&quot;:&quot;Il2Hl-Bn8c2KcDEGtaT9O&quot;,&quot;hasEnterpriseEligibleOrg&quot;:false}">

<header class="from-gray-50-to-white bg-linear-to-t relative z-40 border-b border-gray-100 via-white pt-0.5 dark:via-gray-950"><div class="relative mx-4 mb-1 flex flex-col justify-between max-sm:mt-2 sm:mb-0 xl:flex-row"><div class="flex items-center justify-between xl:min-w-0"><h1 class="my-2 flex w-full min-w-0 flex-wrap items-center gap-y-2 text-lg leading-tight xl:flex-nowrap"><span class="flex shrink-0 flex-nowrap items-center"><a href="/spaces" class="hover:bg-linear-to-r peer order-last hidden font-bold hover:from-blue-600 hover:via-purple-600 hover:to-pink-600 hover:bg-clip-text hover:text-transparent sm:inline">Spaces</a>
							<svg class="hidden peer-hover:block mr-1.5 w-5 animate__animated animate__fadeInUp animate__fast" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M7.80914 18.7462V24.1907H13.2536V18.7462H7.80914Z" fill="#FF3270"></path><path d="M18.7458 18.7462V24.1907H24.1903V18.7462H18.7458Z" fill="#861FFF"></path><path d="M7.80914 7.80982V13.2543H13.2536V7.80982H7.80914Z" fill="#097EFF"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M4 6.41775C4 5.08246 5.08246 4 6.41775 4H14.6457C15.7626 4 16.7026 4.75724 16.9802 5.78629C18.1505 4.67902 19.7302 4 21.4685 4C25.0758 4 28.0003 6.92436 28.0003 10.5317C28.0003 12.27 27.3212 13.8497 26.2139 15.02C27.243 15.2977 28.0003 16.2376 28.0003 17.3545V25.5824C28.0003 26.9177 26.9177 28.0003 25.5824 28.0003H17.0635H14.9367H6.41775C5.08246 28.0003 4 26.9177 4 25.5824V15.1587V14.9367V6.41775ZM7.80952 7.80952V13.254H13.254V7.80952H7.80952ZM7.80952 24.1907V18.7462H13.254V24.1907H7.80952ZM18.7462 24.1907V18.7462H24.1907V24.1907H18.7462ZM18.7462 10.5317C18.7462 9.0283 19.9651 7.80952 21.4685 7.80952C22.9719 7.80952 24.1907 9.0283 24.1907 10.5317C24.1907 12.0352 22.9719 13.254 21.4685 13.254C19.9651 13.254 18.7462 12.0352 18.7462 10.5317Z" fill="black"></path><path d="M21.4681 7.80982C19.9647 7.80982 18.7458 9.02861 18.7458 10.5321C18.7458 12.0355 19.9647 13.2543 21.4681 13.2543C22.9715 13.2543 24.1903 12.0355 24.1903 10.5321C24.1903 9.02861 22.9715 7.80982 21.4681 7.80982Z" fill="#FFD702"></path></svg>
							<a href="/" class="mr-0 w-5 peer-hover:hidden sm:mr-1.5"><img alt="Hugging Face's logo" src="/front/assets/huggingface_logo-noborder.svg" class="w-5"></a></span>
						<hr class="rounded-xs mx-2 h-2 translate-y-px border-r dark:border-gray-600 xl:mx-2.5">
						<div class="group flex flex-none items-center"><div class="relative mr-1 flex items-center">

			

<span class="inline-block "><span class="contents"><a href="/garywelz" class="text-gray-400 hover:text-blue-600"><img alt="" class="size-3.5 rounded-full  flex-none" src="https://cdn-avatars.huggingface.co/v1/production/uploads/67c75cdd2e547a123098b091/Z0x0RIn4jBulG2IgNVx8J.jpeg" crossorigin="anonymous"></a></span>
	</span></div>
		

<span class="inline-block "><span class="contents"><a href="/garywelz" class="text-gray-400 hover:text-blue-600">garywelz</a></span>
	</span>
		<div class="mx-0.5 text-gray-300">/</div></div>

<div class="max-w-full xl:flex xl:min-w-0 xl:flex-nowrap xl:items-center xl:gap-x-1"><a class="break-words font-mono font-semibold hover:text-blue-600 text-[1.07rem] xl:truncate" href="/spaces/garywelz/glmp">glmp</a>
	<button class="text-xs mr-3  focus:outline-hidden inline-flex cursor-pointer items-center text-sm  mx-0.5   text-gray-600 " title="Copy space name to clipboard" type="button"><svg class="" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="currentColor" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M28,10V28H10V10H28m0-2H10a2,2,0,0,0-2,2V28a2,2,0,0,0,2,2H28a2,2,0,0,0,2-2V10a2,2,0,0,0-2-2Z" transform="translate(0)"></path><path d="M4,18H2V4A2,2,0,0,1,4,2H18V4H4Z" transform="translate(0)"></path><rect fill="none" width="32" height="32"></rect></svg>
		</button></div>
						<div class="inline-flex items-center overflow-hidden whitespace-nowrap rounded-md border bg-white text-sm leading-none text-gray-500  mr-2 shrink-0"><button class="relative flex items-center overflow-hidden from-red-50 to-transparent dark:from-red-900 px-1.5 py-1 hover:bg-linear-to-t focus:outline-hidden"  title="Unlike"><svg class="left-1.5 absolute" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32" fill="currentColor"><path d="M22.45,6a5.47,5.47,0,0,1,3.91,1.64,5.7,5.7,0,0,1,0,8L16,26.13,5.64,15.64a5.7,5.7,0,0,1,0-8,5.48,5.48,0,0,1,7.82,0L16,10.24l2.53-2.58A5.44,5.44,0,0,1,22.45,6m0-2a7.47,7.47,0,0,0-5.34,2.24L16,7.36,14.89,6.24a7.49,7.49,0,0,0-10.68,0,7.72,7.72,0,0,0,0,10.82L16,29,27.79,17.06a7.72,7.72,0,0,0,0-10.82A7.49,7.49,0,0,0,22.45,4Z"></path></svg>

		<svg class="absolute text-red-500 origin-center transform transition-transform ease-in
						
						left-1.5 " xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32" fill="currentColor"><path d="M22.5,4c-2,0-3.9,0.8-5.3,2.2L16,7.4l-1.1-1.1C12,3.3,7.2,3.3,4.3,6.2c0,0-0.1,0.1-0.1,0.1c-3,3-3,7.8,0,10.8L16,29l11.8-11.9c3-3,3-7.8,0-10.8C26.4,4.8,24.5,4,22.5,4z"></path></svg>
		<span class="ml-4 pl-0.5 ">like</span></button>
	<button class="focus:outline-hidden flex items-center border-l px-1.5 py-1 text-gray-400 hover:bg-gray-50 focus:bg-gray-100 dark:hover:bg-gray-900 dark:focus:bg-gray-800" title="See users who liked this repository">1</button></div>




						
						
						



<span class="inline-block "><span class="contents"><div class="cursor-pointer select-none overflow-hidden font-mono text-xs shrink-0 mr-2 flex items-center rounded-lg border leading-none dark:bg-gray-900
					border-green-100 
					text-green-700 dark:text-green-500"><div class="inline-flex items-center px-2 py-[0.32rem] dark:bg-gray-900  border-green-100 bg-green-50 hover:bg-green-100/70 hover:text-green-800 dark:hover:text-green-400">
					<div class="ml-0.5 mr-1.5 inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-green-500"></div>
		Running
		</div>
	</div></span>
	</span>

	



						

<div class="xl:hidden"><div class="relative ">
	<button class="btn px-1 py-1 text-sm translate-y-0 " type="button">
		
			<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="p-px" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><circle cx="16" cy="7" r="3" fill="currentColor"></circle><circle cx="16" cy="16" r="3" fill="currentColor"></circle><circle cx="16" cy="25" r="3" fill="currentColor"></circle></svg>
			
		
		</button>
	
	
	</div></div>





</h1>

					<div class="flex flex-none items-center justify-center p-0.5 place-self-start p-0 max-sm:absolute max-sm:-right-4 max-sm:-top-2 sm:my-2 xl:hidden aspect-1"><button class="relative z-40 flex h-6 w-8 items-center justify-center" type="button"><svg width="1em" height="1em" viewBox="0 0 10 10" class="text-xl" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" preserveAspectRatio="xMidYMid meet" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.65039 2.9999C1.65039 2.8066 1.80709 2.6499 2.00039 2.6499H8.00039C8.19369 2.6499 8.35039 2.8066 8.35039 2.9999C8.35039 3.1932 8.19369 3.3499 8.00039 3.3499H2.00039C1.80709 3.3499 1.65039 3.1932 1.65039 2.9999ZM1.65039 4.9999C1.65039 4.8066 1.80709 4.6499 2.00039 4.6499H8.00039C8.19369 4.6499 8.35039 4.8066 8.35039 4.9999C8.35039 5.1932 8.19369 5.3499 8.00039 5.3499H2.00039C1.80709 5.3499 1.65039 5.1932 1.65039 4.9999ZM2.00039 6.6499C1.80709 6.6499 1.65039 6.8066 1.65039 6.9999C1.65039 7.1932 1.80709 7.3499 2.00039 7.3499H8.00039C8.19369 7.3499 8.35039 7.1932 8.35039 6.9999C8.35039 6.8066 8.19369 6.6499 8.00039 6.6499H2.00039Z"></path></svg>
		</button>

	</div></div>

				<div class="hidden flex-row items-center justify-between gap-x-2 xl:flex xl:flex-none"><div class="-mb-px flex h-12 items-center overflow-x-auto overflow-y-hidden ">
	<a class="tab-alternate active" href="/spaces/garywelz/glmp"><svg class="mr-1.5 text-gray-400 flex-none" style="" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path class="uim-quaternary" d="M20.23 7.24L12 12L3.77 7.24a1.98 1.98 0 0 1 .7-.71L11 2.76c.62-.35 1.38-.35 2 0l6.53 3.77c.29.173.531.418.7.71z" opacity=".25" fill="currentColor"></path><path class="uim-tertiary" d="M12 12v9.5a2.09 2.09 0 0 1-.91-.21L4.5 17.48a2.003 2.003 0 0 1-1-1.73v-7.5a2.06 2.06 0 0 1 .27-1.01L12 12z" opacity=".5" fill="currentColor"></path><path class="uim-primary" d="M20.5 8.25v7.5a2.003 2.003 0 0 1-1 1.73l-6.62 3.82c-.275.13-.576.198-.88.2V12l8.23-4.76c.175.308.268.656.27 1.01z" fill="currentColor"></path></svg>
	App
	

	
		</a><a class="tab-alternate" href="/spaces/garywelz/glmp/tree/main"><svg class="mr-1.5 text-gray-400 flex-none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path class="uim-tertiary" d="M21 19h-8a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2zm0-4h-8a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2zm0-8h-8a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2zm0 4h-8a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2z" opacity=".5" fill="currentColor"></path><path class="uim-primary" d="M9 19a1 1 0 0 1-1-1V6a1 1 0 0 1 2 0v12a1 1 0 0 1-1 1zm-6-4.333a1 1 0 0 1-.64-1.769L3.438 12l-1.078-.898a1 1 0 0 1 1.28-1.538l2 1.667a1 1 0 0 1 0 1.538l-2 1.667a.999.999 0 0 1-.64.231z" fill="currentColor"></path></svg>
	<span class="xl:hidden">Files</span>
		<span class="hidden xl:inline">Files</span>
	

	
		</a><a class="tab-alternate" href="/spaces/garywelz/glmp/discussions"><svg class="mr-1.5 text-gray-400 flex-none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M20.6081 3C21.7684 3 22.8053 3.49196 23.5284 4.38415C23.9756 4.93678 24.4428 5.82749 24.4808 7.16133C24.9674 7.01707 25.4353 6.93643 25.8725 6.93643C26.9833 6.93643 27.9865 7.37587 28.696 8.17411C29.6075 9.19872 30.0124 10.4579 29.8361 11.7177C29.7523 12.3177 29.5581 12.8555 29.2678 13.3534C29.8798 13.8646 30.3306 14.5763 30.5485 15.4322C30.719 16.1032 30.8939 17.5006 29.9808 18.9403C30.0389 19.0342 30.0934 19.1319 30.1442 19.2318C30.6932 20.3074 30.7283 21.5229 30.2439 22.6548C29.5093 24.3704 27.6841 25.7219 24.1397 27.1727C21.9347 28.0753 19.9174 28.6523 19.8994 28.6575C16.9842 29.4379 14.3477 29.8345 12.0653 29.8345C7.87017 29.8345 4.8668 28.508 3.13831 25.8921C0.356375 21.6797 0.754104 17.8269 4.35369 14.1131C6.34591 12.058 7.67023 9.02782 7.94613 8.36275C8.50224 6.39343 9.97271 4.20438 12.4172 4.20438H12.4179C12.6236 4.20438 12.8314 4.2214 13.0364 4.25468C14.107 4.42854 15.0428 5.06476 15.7115 6.02205C16.4331 5.09583 17.134 4.359 17.7682 3.94323C18.7242 3.31737 19.6794 3 20.6081 3ZM20.6081 5.95917C20.2427 5.95917 19.7963 6.1197 19.3039 6.44225C17.7754 7.44319 14.8258 12.6772 13.7458 14.7131C13.3839 15.3952 12.7655 15.6837 12.2086 15.6837C11.1036 15.6837 10.2408 14.5497 12.1076 13.1085C14.9146 10.9402 13.9299 7.39584 12.5898 7.1776C12.5311 7.16799 12.4731 7.16355 12.4172 7.16355C11.1989 7.16355 10.6615 9.33114 10.6615 9.33114C10.6615 9.33114 9.0863 13.4148 6.38031 16.206C3.67434 18.998 3.5346 21.2388 5.50675 24.2246C6.85185 26.2606 9.42666 26.8753 12.0653 26.8753C14.8021 26.8753 17.6077 26.2139 19.1799 25.793C19.2574 25.7723 28.8193 22.984 27.6081 20.6107C27.4046 20.212 27.0693 20.0522 26.6471 20.0522C24.9416 20.0522 21.8393 22.6726 20.5057 22.6726C20.2076 22.6726 19.9976 22.5416 19.9116 22.222C19.3433 20.1173 28.552 19.2325 27.7758 16.1839C27.639 15.6445 27.2677 15.4256 26.746 15.4263C24.4923 15.4263 19.4358 19.5181 18.3759 19.5181C18.2949 19.5181 18.2368 19.4937 18.2053 19.4419C17.6743 18.557 17.9653 17.9394 21.7082 15.6009C25.4511 13.2617 28.0783 11.8545 26.5841 10.1752C26.4121 9.98141 26.1684 9.8956 25.8725 9.8956C23.6001 9.89634 18.2311 14.9403 18.2311 14.9403C18.2311 14.9403 16.7821 16.496 15.9057 16.496C15.7043 16.496 15.533 16.4139 15.4169 16.2112C14.7956 15.1296 21.1879 10.1286 21.5484 8.06535C21.7928 6.66715 21.3771 5.95917 20.6081 5.95917Z" fill="#FF9D00"></path><path d="M5.50686 24.2246C3.53472 21.2387 3.67446 18.9979 6.38043 16.206C9.08641 13.4147 10.6615 9.33111 10.6615 9.33111C10.6615 9.33111 11.2499 6.95933 12.59 7.17757C13.93 7.39581 14.9139 10.9401 12.1069 13.1084C9.29997 15.276 12.6659 16.7489 13.7459 14.713C14.8258 12.6772 17.7747 7.44316 19.304 6.44221C20.8326 5.44128 21.9089 6.00204 21.5484 8.06532C21.188 10.1286 14.795 15.1295 15.4171 16.2118C16.0391 17.2934 18.2312 14.9402 18.2312 14.9402C18.2312 14.9402 25.0907 8.49588 26.5842 10.1752C28.0776 11.8545 25.4512 13.2616 21.7082 15.6008C17.9646 17.9393 17.6744 18.557 18.2054 19.4418C18.7372 20.3266 26.9998 13.1351 27.7759 16.1838C28.5513 19.2324 19.3434 20.1173 19.9117 22.2219C20.48 24.3274 26.3979 18.2382 27.6082 20.6107C28.8193 22.9839 19.2574 25.7722 19.18 25.7929C16.0914 26.62 8.24723 28.3726 5.50686 24.2246Z" fill="#FFD21E"></path></svg>
	Community
	

	
		</a><a class="tab-alternate" href="/spaces/garywelz/glmp/settings"><svg class="opacity-50 dark:opacity-70 mr-1.5 text-gray-400 flex-none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 25 25" fill="currentColor"><path d="M13.0101 3C13.7157 3.0078 14.4184 3.09062 15.1077 3.24652C15.2543 3.2797 15.3871 3.35848 15.4874 3.47186C15.5877 3.58523 15.6506 3.72754 15.6672 3.8789L15.8306 5.36678C15.8537 5.57655 15.925 5.77791 16.0389 5.95464C16.1527 6.13137 16.3059 6.27854 16.4861 6.38432C16.6663 6.4901 16.8685 6.55153 17.0764 6.56367C17.2843 6.57581 17.4921 6.53831 17.6831 6.4542L19.0299 5.85495C19.1667 5.79391 19.3187 5.77743 19.4651 5.8078C19.6115 5.83818 19.745 5.9139 19.847 6.02449C20.8199 7.07789 21.5443 8.3412 21.9658 9.71937C22.01 9.8642 22.0087 10.0194 21.962 10.1634C21.9153 10.3074 21.8256 10.4332 21.7053 10.5232L20.5113 11.4158C20.3434 11.5408 20.2069 11.7041 20.1128 11.8925C20.0187 12.0809 19.9697 12.2891 19.9697 12.5003C19.9697 12.7114 20.0187 12.9196 20.1128 13.108C20.2069 13.2964 20.3434 13.4597 20.5113 13.5848L21.7062 14.4763C21.8269 14.5663 21.917 14.6922 21.9638 14.8364C22.0107 14.9806 22.0121 15.1361 21.9677 15.2812C21.546 16.6593 20.8216 17.9225 19.849 18.976C19.7471 19.0864 19.6141 19.162 19.4681 19.1926C19.3221 19.2231 19.1704 19.207 19.0338 19.1466L17.6812 18.5454C17.4904 18.4606 17.2827 18.4225 17.0748 18.4343C16.8668 18.446 16.6645 18.5072 16.4842 18.6129C16.3039 18.7185 16.1508 18.8658 16.037 19.0426C15.9233 19.2195 15.8523 19.421 15.8297 19.6308L15.6672 21.1177C15.6508 21.2674 15.5892 21.4084 15.4908 21.5212C15.3923 21.6341 15.2619 21.7133 15.1173 21.7482C13.7249 22.0839 12.2742 22.0839 10.8817 21.7482C10.7371 21.7133 10.6067 21.6341 10.5083 21.5212C10.4098 21.4084 10.3482 21.2674 10.3318 21.1177L10.1703 19.6328C10.1468 19.4235 10.0751 19.2227 9.96107 19.0465C9.84703 18.8704 9.69381 18.7238 9.51373 18.6186C9.33364 18.5134 9.13172 18.4525 8.92419 18.4408C8.71666 18.4291 8.50931 18.4669 8.31882 18.5512L6.9672 19.1514C6.83048 19.2121 6.67854 19.2283 6.53235 19.1978C6.38616 19.1672 6.25292 19.0915 6.15103 18.9809C5.17789 17.9263 4.45346 16.6616 4.03227 15.2821C3.98795 15.1371 3.98931 14.9816 4.03617 14.8374C4.08304 14.6931 4.17306 14.5673 4.29375 14.4773L5.48868 13.5848C5.65676 13.4599 5.79345 13.2966 5.88768 13.1082C5.9819 12.9198 6.031 12.7115 6.031 12.5003C6.031 12.289 5.9819 12.0808 5.88768 11.8923C5.79345 11.7039 5.65676 11.5407 5.48868 11.4158L4.29375 10.5252C4.17324 10.4351 4.0834 10.3092 4.03671 10.1649C3.99003 10.0207 3.98881 9.8653 4.03323 9.72034C4.45479 8.34219 5.17922 7.07889 6.15199 6.02547C6.25407 5.91487 6.38753 5.83915 6.53391 5.80878C6.6803 5.77841 6.83238 5.79488 6.96912 5.85593L8.31498 6.45517C8.5063 6.53923 8.71441 6.57664 8.92258 6.56439C9.13075 6.55214 9.33319 6.49057 9.51363 6.38462C9.69406 6.27868 9.84747 6.13132 9.96152 5.95438C10.0756 5.77744 10.1471 5.57585 10.1703 5.36581L10.3338 3.8789C10.3503 3.72724 10.4132 3.58462 10.5137 3.47103C10.6142 3.35745 10.7473 3.2786 10.8942 3.24555C11.5835 3.09062 12.2881 3.00877 13.0101 3ZM12.9986 9.57711C12.2337 9.57711 11.5001 9.88508 10.9593 10.4333C10.4184 10.9815 10.1146 11.725 10.1146 12.5003C10.1146 13.2755 10.4184 14.0191 10.9593 14.5672C11.5001 15.1154 12.2337 15.4234 12.9986 15.4234C13.7634 15.4234 14.497 15.1154 15.0378 14.5672C15.5787 14.0191 15.8825 13.2755 15.8825 12.5003C15.8825 11.725 15.5787 10.9815 15.0378 10.4333C14.497 9.88508 13.7634 9.57711 12.9986 9.57711Z"></path></svg>
	Settings
	

	
		</a></div>

					

<div class="mt-0"><div class="relative ">
	<button class="btn px-1 py-1 text-base translate-y-px " type="button">
		
			<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="p-0.5" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><circle cx="16" cy="7" r="3" fill="currentColor"></circle><circle cx="16" cy="16" r="3" fill="currentColor"></circle><circle cx="16" cy="25" r="3" fill="currentColor"></circle></svg>
			
		
		</button>
	
	
	</div></div>






					<hr class="rounded-xs ml-2 h-2 translate-y-px border-r dark:border-gray-600">
						<form action="/logout" method="POST" class="hidden"><input type="hidden" name="csrf" value="eyJkYXRhIjp7ImV4cGlyYXRpb24iOjE3NTU2MjQyODExMDUsInVzZXJJZCI6IjY3Yzc1Y2RkMmU1NDdhMTIzMDk4YjA5MSJ9LCJzaWduYXR1cmUiOiIyMzZmODk3MDNjOTA3NmY3MTY3OTg5NDIwZTRmNTUzNmE0MGNkYjk1OGVlNTFmNWYzMWIwYWVkOGYyZjA4YTJkIn0="></form>
<div class="relative ml-2 w-[1.38rem] h-[1.38rem] mr-2">
	<button class="ml-auto rounded-full ring-2 group ring-indigo-400 focus:ring-blue-500 hover:ring-offset-1 focus:ring-offset-1 focus:outline-hidden outline-hidden dark:ring-offset-gray-950 " type="button">
		
		<div class="relative"><img alt="" class="h-[1.38rem] w-[1.38rem] overflow-hidden rounded-full" src="https://cdn-avatars.huggingface.co/v1/production/uploads/67c75cdd2e547a123098b091/Z0x0RIn4jBulG2IgNVx8J.jpeg" crossorigin="anonymous">
			</div>
	
		</button>
	
	
	</div></div></div>
			</header>























	







</div>
	
	
	
	<div class="SVELTE_HYDRATER contents" data-target="SSOBanner" data-props="{&quot;organizations&quot;:[]}"></div>
	


	

	<main class="flex flex-1 flex-col">
	
	

	<div class="SVELTE_HYDRATER contents" data-target="SpacePageInner" data-props="{&quot;authLight&quot;:{&quot;csrfToken&quot;:&quot;eyJkYXRhIjp7ImV4cGlyYXRpb24iOjE3NTU2MjQyODExMDUsInVzZXJJZCI6IjY3Yzc1Y2RkMmU1NDdhMTIzMDk4YjA5MSJ9LCJzaWduYXR1cmUiOiIyMzZmODk3MDNjOTA3NmY3MTY3OTg5NDIwZTRmNTUzNmE0MGNkYjk1OGVlNTFmNWYzMWIwYWVkOGYyZjA4YTJkIn0=&quot;,&quot;hasHfLevelAccess&quot;:false,&quot;u&quot;:{&quot;avatarUrl&quot;:&quot;https://cdn-avatars.huggingface.co/v1/production/uploads/67c75cdd2e547a123098b091/Z0x0RIn4jBulG2IgNVx8J.jpeg&quot;,&quot;isPro&quot;:false,&quot;orgs&quot;:[],&quot;user&quot;:&quot;garywelz&quot;,&quot;canPost&quot;:false,&quot;canHaveBilling&quot;:true,&quot;canCreateOrg&quot;:true,&quot;theme&quot;:&quot;light&quot;,&quot;notifications&quot;:{&quot;org_suggestions&quot;:false},&quot;hardwareItems&quot;:[],&quot;hardwareItemsPrivate&quot;:false,&quot;usage&quot;:{&quot;storage&quot;:{&quot;used&quot;:52107958,&quot;usedPrivate&quot;:0,&quot;usedPublic&quot;:52107958,&quot;count&quot;:2,&quot;limit&quot;:100000000000,&quot;summary&quot;:{&quot;space&quot;:{&quot;used&quot;:52107958,&quot;usedPrivate&quot;:0,&quot;usedPublic&quot;:52107958,&quot;count&quot;:2}}},&quot;inference&quot;:{&quot;usedNanoUsd&quot;:0,&quot;numRequests&quot;:0,&quot;providerDetails&quot;:[],&quot;periodEnd&quot;:&quot;2025-08-31T23:59:59.999Z&quot;,&quot;periodStart&quot;:&quot;2025-08-01T00:00:00.000Z&quot;,&quot;includedNanoUsd&quot;:100000000,&quot;limitNanoUsd&quot;:100000000,&quot;lastUpdated&quot;:&quot;2025-08-18T17:24:20.798Z&quot;},&quot;zeroGpu&quot;:{&quot;base&quot;:210,&quot;current&quot;:210,&quot;lastUpdated&quot;:&quot;2025-08-18T17:24:20.798Z&quot;}},&quot;welcomeLinks&quot;:[]}},&quot;canRestart&quot;:true,&quot;canWrite&quot;:true,&quot;csrf&quot;:&quot;eyJkYXRhIjp7ImV4cGlyYXRpb24iOjE3NTU2MjQyODExMDUsInVzZXJJZCI6IjY3Yzc1Y2RkMmU1NDdhMTIzMDk4YjA5MSJ9LCJzaWduYXR1cmUiOiIyMzZmODk3MDNjOTA3NmY3MTY3OTg5NDIwZTRmNTUzNmE0MGNkYjk1OGVlNTFmNWYzMWIwYWVkOGYyZjA4YTJkIn0=&quot;,&quot;hideNFAA&quot;:false,&quot;readmeTemplate&quot;:&quot;---\ntitle: {{title}}\nemoji: {{emoji}}\ncolorFrom: {{colorFrom}}\ncolorTo: {{colorTo}}\nsdk: {{sdk}}\nsdk_version: \&quot;{{sdkVersion}}\&quot;\napp_file: app.py\npinned: false\n---\n\nCheck out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference\n&quot;,&quot;space&quot;:{&quot;author&quot;:&quot;garywelz&quot;,&quot;colorFrom&quot;:&quot;blue&quot;,&quot;colorTo&quot;:&quot;green&quot;,&quot;cardData&quot;:{&quot;title&quot;:&quot;Genome Logic Modeling Project (GLMP)&quot;,&quot;emoji&quot;:&quot;🧬&quot;,&quot;colorFrom&quot;:&quot;blue&quot;,&quot;colorTo&quot;:&quot;green&quot;,&quot;sdk&quot;:&quot;static&quot;,&quot;sdk_version&quot;:&quot;latest&quot;,&quot;app_file&quot;:&quot;README.md&quot;,&quot;pinned&quot;:false},&quot;createdAt&quot;:&quot;2025-07-28T19:47:08.000Z&quot;,&quot;emoji&quot;:&quot;🧬&quot;,&quot;discussionsDisabled&quot;:false,&quot;duplicationDisabled&quot;:false,&quot;id&quot;:&quot;garywelz/glmp&quot;,&quot;isLikedByUser&quot;:true,&quot;watched&quot;:{&quot;isWatching&quot;:true,&quot;isMuted&quot;:false,&quot;mode&quot;:&quot;global&quot;},&quot;lastModified&quot;:&quot;2025-08-18T16:35:58.000Z&quot;,&quot;likes&quot;:1,&quot;pinned&quot;:false,&quot;private&quot;:false,&quot;gated&quot;:false,&quot;repoType&quot;:&quot;space&quot;,&quot;subdomain&quot;:&quot;garywelz-glmp&quot;,&quot;sdk&quot;:&quot;static&quot;,&quot;sdkVersion&quot;:&quot;latest&quot;,&quot;staticOrigin&quot;:&quot;README.md&quot;,&quot;title&quot;:&quot;Genome Logic Modeling Project (GLMP)&quot;,&quot;runtime&quot;:{&quot;stage&quot;:&quot;RUNNING&quot;,&quot;hardware&quot;:{&quot;current&quot;:null,&quot;requested&quot;:null},&quot;storage&quot;:null,&quot;replicas&quot;:{&quot;requested&quot;:1,&quot;current&quot;:1}},&quot;iframe&quot;:{&quot;embedSrc&quot;:&quot;https://garywelz-glmp.static.hf.space&quot;,&quot;src&quot;:&quot;https://garywelz-glmp.static.hf.space/README.md&quot;},&quot;secrets&quot;:[],&quot;variables&quot;:[],&quot;linkedModels&quot;:[],&quot;linkedDatasets&quot;:[],&quot;linkedCollections&quot;:[],&quot;sha&quot;:&quot;b8ec5961c9d22b5b3b686d476c495e92c45b7864&quot;,&quot;hasBlockedOids&quot;:false,&quot;region&quot;:&quot;us&quot;,&quot;tags&quot;:[&quot;static&quot;,&quot;region:us&quot;],&quot;xetEnabled&quot;:false},&quot;iframeSrc&quot;:&quot;https://garywelz-glmp.static.hf.space/README.md&quot;,&quot;showGettingStarted&quot;:false,&quot;sessionUuid&quot;:&quot;Il2Hl-Bn8c2KcDEGtaT9O&quot;,&quot;isStaticHtmlAvailable&quot;:false,&quot;jwt&quot;:{&quot;token&quot;:&quot;eyJhbGciOiJFZERTQSJ9.eyJyZWFkIjp0cnVlLCJwZXJtaXNzaW9ucyI6eyJyZXBvLmNvbnRlbnQucmVhZCI6dHJ1ZX0sIm9uQmVoYWxmT2YiOnsia2luZCI6InVzZXIiLCJfaWQiOiI2N2M3NWNkZDJlNTQ3YTEyMzA5OGIwOTEiLCJ1c2VyIjoiZ2FyeXdlbHoiLCJpc1BybyI6ZmFsc2UsImlzRW50ZXJwcmlzZU1lbWJlciI6ZmFsc2UsInNlc3Npb25JZCI6IjY4OThkYTc5M2M3ZDcyZDVkYzgyMzExOSJ9LCJpYXQiOjE3NTU1Mzc4ODEsInN1YiI6Ii9zcGFjZXMvZ2FyeXdlbHovZ2xtcCIsImV4cCI6MTc1NTUzODA2MSwiaXNzIjoiaHR0cHM6Ly9odWdnaW5nZmFjZS5jbyJ9.Nw13Royx_8z7VFIS7SBk23o6XfNSAjGVOPGRTzQzPeOy7kvhWedz1C1jSQ9Th35R8mSByaJKqUNl19loxyjsCw&quot;,&quot;expiration&quot;:180000}}">


<div class="spinner-overlay fixed inset-0 flex h-full w-full items-center justify-center overflow-y-auto bg-gray-500 text-white opacity-80 hidden"><svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" fill="none" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
	<span>Refreshing</span></div>


	<iframe src="https://garywelz-glmp.static.hf.space/README.md" aria-label="static space app" class="space-iframe outline-hidden grow bg-white p-0" allow="accelerometer; ambient-light-sensor; autoplay; battery; camera; clipboard-read; clipboard-write; display-capture; document-domain; encrypted-media; fullscreen; geolocation; gyroscope; layout-animations; legacy-image-formats; magnetometer; microphone; midi; oversized-images; payment; picture-in-picture; publickey-credentials-get; serial; sync-xhr; usb; vr ; wake-lock; xr-spatial-tracking" sandbox="allow-downloads allow-forms allow-modals allow-pointer-lock allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-storage-access-by-user-activation" scrolling="yes"></iframe>

		

</div></main>

	</div>

		<script>
			import("\/front\/build\/kube-838da81\/index.js");
			window.moonSha = "kube-838da81\/";
			window.__hf_deferred = {};
		</script>

		<!-- Stripe -->
		<script>
			if (["hf.co", "huggingface.co"].includes(window.location.hostname)) {
				const script = document.createElement("script");
				script.src = "https://js.stripe.com/v3/";
				script.async = true;
				document.head.appendChild(script);
			}
		</script>
	</body>
</html>
