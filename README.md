# UA-MRI Lab Website

This is the web page codebase for the UA-MRI (University of Arizona Magnetic Resonance Imaging) Lab website.

## Adding a New Person to the Team Page

To add a new team member to the people page, follow these steps:

### Step 1: Create a Markdown File

Create a new markdown file in the `_people/` folder. The filename should be in the format: `firstname_lastname.md` (e.g., `deniz_karakay.md`).

### Step 2: Use the Template

Copy the structure from an existing profile. You can use `_people/deniz_karakay.md` as a reference example:

```yaml
---
layout: profile
name: Your Full Name
title: Your Position Title
permalink: /people/your-name/

# Profile card data (used for people page)
category: Students  # Options: Faculty, Students, or Alumni
order: 1  # Number for ordering within category (1, 2, 3, etc.)
image: people/your_image.jpg  # Path to image in assets/img/ folder
image_circular: true  # Set to true for circular image, false for square
email: your.email@arizona.edu
github: https://github.com/yourusername  # Optional
website: https://yourwebsite.com  # Optional
linkedin: https://www.linkedin.com/in/yourprofile  # Optional
scholar: https://scholar.google.com/citations?user=YOUR_ID  # Optional
more_info: >
  <p><strong>Research:</strong> Your research interests</p>

profile:
  align: right  # Options: left or right (image position on profile page)
  image: people/your_image.jpg  # Same as above
  image_circular: true
  more_info: >
    <p><strong>Email:</strong> your.email@arizona.edu</p>
    <p><strong>Research:</strong> Your research interests</p>

social: false  # Set to true if you want social icons at bottom of page
---

Write your detailed biography here. This is your personal profile page where you can add:

- Your research interests
- Your background and education
- Publications
- Projects you're working on
- Any other information you'd like to share

You can use markdown formatting, include images, links, and more.
```

### Step 3: Add Your Profile Image

1. Place your profile image in the `assets/img/people/` folder
2. Use a descriptive filename (e.g., `firstname_lastname.jpg` or `firstname_lastname.png`)
3. **Important**: Images should be **square** (equal width and height, e.g., 500x500px or 1000x1000px) for the best appearance, especially when using `image_circular: true`
4. Update the `image` field in your markdown file to match the filename (e.g., `image: people/your_image.jpg`)

For questions or issues, please contact the website maintainer.
