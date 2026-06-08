---
name: automated-blog-publisher
description: End-to-end automated blog publishing workflow - from RSS news monitoring to SEO-optimized content creation and Git deployment
version: 1.0.0
author: Hermes Agent
tags: [blog, automation, rss, seo, git, content-creation]
---

# Automated Blog Publisher

A comprehensive workflow for automatically discovering trending topics, writing SEO-optimized blog posts, and deploying them to a Git-based blog platform.

## Overview

This skill implements a complete automated blog publishing pipeline:
1. **RSS Monitoring**: Track multiple tech/news sources for recent content
2. **Topic Selection**: Filter for relevant, non-duplicate topics within specified scope
3. **Content Creation**: Write SEO-optimized articles following existing blog format
4. **Media Management**: Handle images (generate or use fallback URLs)
5. **Git Deployment**: Commit and push articles automatically
6. **Notifications**: Send completion notifications

## Prerequisites

### Required Tools
- **Primary Option**: `blogwatcher-cli` - RSS feed monitoring
- **Alternative Option**: Browser tools for direct site navigation
- Git - Version control for blog content
- Text editor - Content creation (handled by Hermes)

### Setup Commands
```bash
# Install blogwatcher CLI (RSS-based approach)
go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest

# Verify installation
which blogwatcher-cli
# Should output: /home/simon/go/bin/blogwatcher-cli
```

### Alternative: Browser-Based Approach
When RSS feeds are unavailable or blocked (common with news sites):
- Use `browser_navigate` to access news sites directly
- Navigate through site structure manually
- Extract content from full article pages
- Handle bot detection gracefully

## Configuration

### RSS Feed Setup
Add relevant news sources to blogwatcher:

```bash
# Technology news sources
blogwatcher-cli add "TechCrunch" https://techcrunch.com/feed/
blogwatcher-cli add "MIT Technology Review" https://www.technologyreview.com/feed/
blogwatcher-cli add "The Verge" https://www.theverge.com/rss/index.xml

# Business/Finance sources
blogwatcher-cli add "Reuters Business" https://www.reuters.com/business/ --feed-url https://www.reuters.com/business/rss/

# Add more sources as needed
```

### Blog Configuration
Ensure blog directory structure:
```
~/blog/
├── content/
│   ├── tech/
│   ├── finance/
│   ├── economy/
│   └── ...
├── static/
│   └── images/
└── git repository
```

## Workflow Steps

### 1. News Monitoring & Topic Discovery

#### Method A: RSS Monitoring (Primary)
```bash
# Scan all configured sources
~/go/bin/blogwatcher-cli scan

# Check recent articles
~/go/bin/blogwatcher-cli articles --all | head -20

# Filter by date and topic
~/go/bin/blogwatcher-cli articles --all | grep "2026-05-17"
```

#### Method B: Browser-Based Discovery (Alternative)
When RSS feeds are blocked or unavailable:

```bash
# Navigate directly to news sites
browser_navigate "https://techcrunch.com"
browser_click "AI category link"
browser_snapshot

# Extract recent articles
browser_vision "Extract full article content"
```

**Key Considerations:**
- Monitor sources within 3-hour window for timeliness
- Check existing content to avoid duplicates
- Focus on high-impact topics with lasting relevance
- Prioritize stories with multiple source coverage
- **Handle bot detection**: Use browser tools instead of direct API calls

### 2. Topic Selection Criteria

**Selection Process:**
1. **Relevance**: Must fit blog scope (AI/tech, finance, semiconductors, etc.)
2. **Timeliness**: Published within last 3-6 hours
3. **Impact**: High significance to target audience
4. **Uniqueness**: No existing coverage in blog content
5. **SEO Potential**: Strong keywords and search traffic potential

**Topic Examples:**
- AI technology breakthroughs
- Semiconductor industry news
- Financial market trends
- Policy changes affecting tech
- Company announcements (Apple, Google, NVIDIA, etc.)

### 3. Content Creation

**Article Structure:**
```yaml
---
title: "SEO-Optimized Title in Chinese"
date: 2026-05-17T08:00:00+08:00
description: "Compelling meta description"
categories:
  - "科技"  # or appropriate category
tags:
  - "Tag1"
  - "Tag2"
  - "Tag3"
image: "https://images.unsplash.com/...?w=800&q=80"
readingTime: 8-12  # estimated reading time
draft: false
faq:
  - q: "Key question 1"
    a: "Comprehensive answer"
  - q: "Key question 2"  
    a: "Detailed explanation"
---
```

**Content Guidelines:**
- Write in Traditional Chinese (繁體中文)
- Include SEO-optimized title and description
- Structure with clear headings and subheadings
- Add 4-6 comprehensive FAQ sections
- Include relevant Taiwan/regional implications
- Maintain professional tone with accessibility
- Target 8-12 minute reading time

### 4. Image Handling

**Image Sources:**
- **Primary**: Use `image_generate` tool when available
- **Fallback**: Use Unsplash URLs with proper sizing (when image_generate unavailable)
- **Format**: `https://images.unsplash.com/photo-xxx?w=800&q=80`

**Image Directory Structure:**
```
~/blog/static/images/
├── tech/
├── finance/
├── economy/
└── ...
```

**Handling Missing Tools:**
When `image_generate` is not available:
```bash
# Create image directory
mkdir -p ~/blog/static/images/[category]

# Use high-quality Unsplash images
# Create attribution file
echo "# Image attribution
# Source: Unsplash
# URL: [image_url]
# Description: [description]" > ~/blog/static/images/[category]/[article]-image.txt
```

**Practical Finding**: Many environments lack image generation tools, so Unsplash fallback should be the primary strategy.

### 5. Git Workflow

```bash
# Navigate to blog directory
cd ~/blog

# Add all changes
git add -A

# Commit with descriptive message
git commit -m "auto: [Article Title]"

# Push to remote repository
git push origin main
```

**Commit Message Format:**
- Prefix with "auto: "
- Use exact article title
- Include date when relevant

### 6. Notification System

**Notification Template:**
```text
新文章發布通知：

標題：[Article Title]
發布時間：[Date]
文章已成功發布到博客，涵蓋了[brief description]。
```

**File Location:** `~/blog/telegram_notification.txt`

**Practical Considerations:**
- Many environments lack `send_message` integration
- Store notification content in text file for manual sending
- Include complete article details for external notification systems

## Error Handling

### Common Issues and Solutions

**RSS Feed Problems:**
```bash
# Remove problematic feeds
blogwatcher-cli remove "Source Name" --yes

# Add with explicit feed URL
blogwatcher-cli add "Source Name" "https://example.com" --feed-url "https://example.com/feed.xml"

# Handle authentication issues by using alternative sources
```

**Git Issues:**
```bash
# Check git status
git status

# Handle merge conflicts if any
git pull origin main
# resolve conflicts
git add -A
git commit -m "resolve conflicts"
git push origin main
```

**Content Validation:**
- Verify frontmatter syntax
- Check for broken links
- Ensure proper categorization
- Validate FAQ format

## Best Practices

### Content Quality
- Maintain consistent writing style
- Include original insights beyond source material
- Add local/regional perspectives (especially for Taiwan audience)
- Keep paragraphs short and scannable
- Use proper markdown formatting

### SEO Optimization
- Research keywords naturally into content
- Create compelling meta descriptions
- Use relevant tags and categories
- Include FAQ sections for featured snippets
- Optimize images with alt text (when available)

### Schedule Management
- Run monitoring during peak news hours
- Allow time for content creation and review
- Buffer time for unexpected delays
- Monitor for breaking news opportunities

## Sample Execution

```bash
# 1. Start monitoring
~/go/bin/blogwatcher-cli scan

# 2. Review recent articles
~/go/bin/blogwatcher-cli articles --all | head -30

# 3. Select and write content (Hermes handles this)
# 4. Create image (use Unsplash URL if needed)
# 5. Git commit and push
cd ~/blog && git add -A && git commit -m "auto: [Title]" && git push

# 6. Create notification
echo "通知內容..." > ~/blog/telegram_notification.txt
```

## Monitoring and Maintenance

### Regular Tasks
- Weekly: Review and update RSS feed list
- Monthly: Analyze top-performing articles
- Quarterly: Update topic selection criteria
- As needed: Troubleshoot feed issues

### Performance Metrics
- Track publish frequency
- Monitor article engagement (if analytics available)
- Measure topic selection success rate
- Track content quality scores

## Troubleshooting

**Blogwatcher Setup:**
```bash
# Check installed location
ls ~/go/bin/blogwatcher-cli

# Verify database location
ls ~/.blogwatcher-cli/

# Test individual feeds
~/go/bin/blogwatcher-cli scan "Specific Source"
```

**Browser-Based Approach Issues:**
```bash
# Handle bot detection
browser_navigate "https://techcrunch.com"  # Avoid direct search queries
browser_click "AI category"               # Navigate through site structure
browser_vision "Extract content"          # Use vision for full content

# Handle blocked content
browser_scroll "down"                     # Reveal more content
browser_console "Extract text content"    # Get article content programmatically
```

**Missing Tools Workarounds:**
- **No web_search**: Use browser_navigate + manual site navigation
- **No image_generate**: Use Unsplash URLs with proper attribution
- **No send_message**: Store notification content in text file

**Content Issues:**
- Check file permissions for blog directory
- Validate frontmatter YAML syntax
- Ensure proper character encoding
- Test image URLs before publishing

**Practical Findings from Recent Execution:**
1. **RSS feeds often blocked**: Browser-based approach more reliable
2. **Bot detection common**: Use browser tools instead of direct API calls
3. **Image generation frequently unavailable**: Unsplash URLs should be primary strategy
4. **Notification tools often missing**: Store content for manual notification

This skill provides a complete framework for automated blog publishing, from content discovery to deployment, with built-in quality controls and error handling.