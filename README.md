# TryScape

TryScape: See yourself in any outfit, anywhere. Our Azure-powered AI generates a photorealistic image of you wearing that look in that location.

## 🚀 Features

- **Responsive Design**: Seamlessly works on desktop, tablet, and mobile devices
- **Interactive UI**: Step-by-step wizard for easy outfit visualization
- **Modern Stack**: Built with Next.js 16, React 19, and Material-UI 7
- **Type-Safe**: Full TypeScript implementation
- **Accessible**: WCAG compliant with proper ARIA labels

## 📸 Screenshots

### Desktop View
![Desktop Home](https://github.com/user-attachments/assets/17e90b51-44d0-4fb0-ac4f-5d79a6da8f77)

### Mobile View
![Mobile Home](https://github.com/user-attachments/assets/362edf0f-cb5c-4a67-a735-f5cb0dfe49f3)

## 🛠️ Tech Stack

- **Framework**: Next.js 16.0.0 (App Router)
- **UI Library**: React 19.2.0
- **Component Library**: Material-UI 7.3.4
- **Styling**: Emotion + Tailwind CSS
- **Language**: TypeScript
- **Icons**: Material Icons

## 📋 Prerequisites

- Node.js 18.x or higher
- npm 9.x or higher

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/SuyashJoshi179/TryScape.git
   cd TryScape
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📜 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Create production build
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## 🎨 How It Works

1. **Upload Your Photo**: Start by uploading a clear photo of yourself
2. **Choose Your Outfit**: Select from our collection of outfits
3. **Pick a Location**: Choose from iconic locations around the world
4. **Generate Image**: Our Azure-powered AI creates your visualization

## 📁 Project Structure

```
TryScape/
├── src/
│   ├── app/              # Next.js app directory
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Main page
│   │   └── globals.css   # Global styles
│   ├── components/       # React components
│   │   ├── Navbar.tsx
│   │   ├── HeroSection.tsx
│   │   ├── HowItWorks.tsx
│   │   ├── GetStarted.tsx
│   │   ├── Footer.tsx
│   │   └── ThemeRegistry.tsx
│   └── theme/            # MUI theme configuration
│       └── theme.ts
├── public/               # Static assets
└── package.json          # Dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- UI components from [Material-UI](https://mui.com/)
- Powered by Azure AI
