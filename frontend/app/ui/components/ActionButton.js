'use client';

import { useRouter } from 'next/navigation';
import styles from '../styles/page.module.css';

export default function ActionButton({ text, type = 'start', route }) {
    const router = useRouter();
    const buttonStyle =
        type === 'primary' ? styles.startButton : styles.aboutButton;

    const handleClick = () => {
        if (route) {
            router.push(route);
        }
    };

    return (
        <button
            className={`${styles.button} ${buttonStyle}`}
            onClick={handleClick}
        >
            {text}
        </button>
    );
}
