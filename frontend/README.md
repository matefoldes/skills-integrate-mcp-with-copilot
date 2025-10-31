# Frontend - Mergington High School Activities

This is the modern React/Next.js frontend for the Mergington High School Activities application, bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

### Prerequisites

- Node.js 18.x or later
- npm, yarn, pnpm, or bun
- Backend API running on `http://localhost:8000`

### Installation

```bash
npm install
```

### Development

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `src/app/page.tsx`. The page auto-updates as you edit the file.

### Building for Production

```bash
npm run build
npm start
```

## Features

- ✨ Modern React with Next.js 16+
- 🎨 Styled with Tailwind CSS
- 📱 Responsive design
- 🔄 Real-time activity updates
- 🎯 TypeScript for type safety
- 🎭 Octocat mascots gallery

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── page.tsx      # Main activities page
│   │   ├── layout.tsx    # Root layout
│   │   └── globals.css   # Global styles
│   └── components/       # Reusable React components (to be added)
├── public/               # Static assets
└── package.json          # Dependencies and scripts
```

## API Integration

The frontend connects to the FastAPI backend:

- `GET /activities` - Fetch all activities with participants
- `POST /activities/{activity_name}/signup?email={email}` - Sign up for an activity
- `DELETE /activities/{activity_name}/unregister?email={email}` - Unregister from an activity

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!
