import "./globals.css";
import type { Metadata } from "next";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "SHF • Autonomous AI Stock Hedge Fund Platform",
  description: "Institutional-Grade Multi-Agent AI Investment Research & Execution Terminal",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-textPrimary antialiased flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
        <footer className="border-t border-borderDark py-4 mt-auto">
          <div className="max-w-7xl mx-auto px-4 text-center text-xs text-textSecondary flex justify-between items-center">
            <span>© 2026 Autonomous AI Stock Hedge Fund (SHF) Architecture</span>
            <span className="text-warning font-semibold">SIMULATION & RESEARCH ONLY • NO REAL TRADES PLACED</span>
          </div>
        </footer>
      </body>
    </html>
  );
}
