import "./globals.css";

export const metadata = {
  title: "California Real Estate AI | House Price Predictor",
  description: "Machine Learning powered California house price estimation and batch valuation tool using FastAPI and Random Forest.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body>
        <div className="bg-mesh" />
        {children}
      </body>
    </html>
  );
}
