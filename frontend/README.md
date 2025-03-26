# Frontend folder structure

```
frontend/
├── app/
│   ├── about/                  # About page route
│   │   └── page.js
│   ├── ui/                     # Shared UI components and styles
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Navbar.js
│   │   │   ├── ActionButton.js
│   │   │   └── TextContainer.js
│   │   ├── styles/             # Centralized styles
│   │   │   └── page.module.css
│   ├── layout.js               # Shared layout
│   └── page.js                 # Default root page
├── public/                     # Static assets
│   ├── pictures/               # Images and assets
│   │   ├── logoLight.png
│   │   ├── logoDark.png
│   │   └── logoAlternative.png
├── node_modules/
├── .gitignore
├── jsconfig.json
├── package.json
├── next.config.mjs
└── eslint.config.mjs
```
