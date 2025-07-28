# Deployment Guide for Genome Logic Modeling Project Website

## 🚀 Quick Start (Local Development)

```bash
# Clone or navigate to your project directory
cd /path/to/your/genome-logic-modeling-project

# Start the local server
python3 serve.py

# Or specify a custom port
python3 serve.py 3000
```

The website will be available at `http://localhost:8000` (or your specified port).

## 🌐 Deployment Options

### Option 1: GitHub Pages (Recommended for Open Source)

1. **Create a GitHub repository** for your project
2. **Push your files** to the repository
3. **Enable GitHub Pages**:
   - Go to repository Settings
   - Scroll to "Pages" section
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)"
   - Your site will be available at `https://yourusername.github.io/genome-logic-modeling`

### Option 2: Netlify (Easy Drag & Drop)

1. **Visit** [netlify.com](https://netlify.com)
2. **Sign up** for a free account
3. **Drag and drop** your project folder to Netlify
4. **Get instant URL** like `https://amazing-pasteur-123456.netlify.app`
5. **Optional**: Connect to GitHub for automatic deployments

### Option 3: Vercel (Great for Scientists)

1. **Visit** [vercel.com](https://vercel.com)
2. **Sign up** with GitHub
3. **Import your repository**
4. **Deploy automatically** - get URL like `https://genome-logic-modeling.vercel.app`

### Option 4: Traditional Web Hosting

Upload all files to any web hosting service:
- **Academic hosting** (many universities provide free hosting)
- **Shared hosting** (BlueHost, SiteGround, etc.)
- **Cloud hosting** (AWS S3, Google Cloud Storage)

## 📁 File Structure for Deployment

```
genome-logic-modeling/
├── index.html                          # Main website
├── docs/
│   └── paper/
│       ├── genome-logic-modeling.md    # Full paper
│       └── figures/                    # Paper figures
├── serve.py                            # Local development server
├── README.md                           # Project documentation
└── DEPLOYMENT.md                       # This file
```

## 🔧 Customization

### Update Contact Information
Edit `index.html` and search for:
- Email links: `gwelz@jjay.cuny.edu`
- GitHub links: `github.com/garywelz`
- Hugging Face links: `huggingface.co/garywelz`

### Add Your Domain
If you have a custom domain:
1. Update all meta tags in `index.html`
2. Change URLs from `genome-logic-modeling.org` to your domain
3. Configure DNS with your hosting provider

### Add Analytics (Optional)
To track visitors, add Google Analytics:
```html
<!-- Add before closing </head> tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 📧 Setting Up Contact Forms

The current site uses `mailto:` links. For better contact management:

### Option 1: Netlify Forms (Free)
Add to any form in HTML:
```html
<form netlify>
  <input type="email" name="email" placeholder="Your email" required>
  <textarea name="message" placeholder="Your message" required></textarea>
  <button type="submit">Send</button>
</form>
```

### Option 2: Formspree (Free tier available)
Create forms at [formspree.io](https://formspree.io) and integrate.

## 🎯 SEO Optimization

The website already includes:
- ✅ Meta descriptions
- ✅ Open Graph tags (Facebook/LinkedIn)
- ✅ Twitter Card tags
- ✅ Semantic HTML structure
- ✅ Mobile-responsive design

### Additional SEO Steps:
1. **Submit to Google Search Console**
2. **Create XML sitemap** (tools like xml-sitemaps.com)
3. **Add schema.org markup** for academic papers
4. **Register with academic search engines** (Google Scholar, CORE, etc.)

## 🔒 Security Considerations

For academic/scientific websites:
- ✅ Use HTTPS (automatic with GitHub Pages, Netlify, Vercel)
- ✅ Keep contact information professional
- ✅ Regular backups of your content
- ✅ Monitor for spam if using contact forms

## 📈 Promoting Your Manifesto

### Academic Channels:
- **Conference presentations** (computational biology, bioinformatics)
- **Academic Twitter** with hashtags: #ComputationalBiology #GenomeLogic #SyntheticBiology
- **ResearchGate** profile and publication
- **ArXiv preprint** for broader visibility
- **Reddit** communities: r/bioinformatics, r/computational_biology, r/MachineLearning

### AI/Tech Channels:
- **Hacker News** submission
- **AI research communities**
- **GitHub trending** (add relevant topics to your repository)
- **LinkedIn articles** for professional network

## 🤝 Collaboration Features

The website is designed to encourage collaboration:
- Clear call-to-action buttons
- Multiple contact methods
- Specific roles for different types of contributors
- Open licensing information
- Link to full academic paper

## 📊 Success Metrics

Track your manifesto's impact:
- **Website visitors** (Google Analytics)
- **Paper downloads** (track PDF downloads)
- **Email inquiries** from potential collaborators
- **GitHub repository stars/forks**
- **Academic citations** (Google Scholar alerts)
- **Social media engagement**

---

## 🆘 Need Help?

- **Technical issues**: Check browser console for errors
- **Content updates**: Edit the markdown file and redeploy
- **Collaboration requests**: Monitor email for inquiries
- **Academic promotion**: Reach out to relevant conferences and journals

Your manifesto is now ready to invite scientists and AI systems to join the quest to understand life as computation! 🧬✨