import { Inter } from 'next/font/google';
import './ui/styles/globals.css';

const interFont = Inter({
    variable: '--font-inter',
    subsets: ['latin'],
});

export const metadata = {
    title: 'Root',
    description:
        'care, track, enjoy. Webpage created for a hackathon. We help people track their plants',
};

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <head>
                <link
                    rel="preconnect"
                    href="https://fonts.googleapis.com"
                ></link>
                <link
                    rel="preconnect"
                    href="https://fonts.gstatic.com"
                    crossorigin
                ></link>
                <link
                    href="https://fonts.googleapis.com/css2?family=Averia+Serif+Libre:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&family=Geist+Mono:wght@100..900&display=swap"
                    rel="stylesheet"
                />
            </head>
            <body className={`${interFont.variable}`}>{children}</body>
        </html>
    );
}
