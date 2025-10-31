import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mergington High School Activities",
  description: "View and sign up for extracurricular activities at Mergington High School",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
