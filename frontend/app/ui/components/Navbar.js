import Image from 'next/image';
import Link from 'next/link';
import styles from '../styles/page.module.css';

export default function Navbar() {
    return (
        <nav className={styles.navBar}>
            <div className={styles.navLogo}>
                <Link href="/">
                    <Image
                        src={'/pictures/logoAlternative.png'}
                        alt="Logo"
                        width={90}
                        height={80}
                        style={{ cursor: 'pointer' }}
                    />
                </Link>
            </div>
            {/* Optional dock or buttons if needed */}
            {/* <div className={styles.navDock}>Dock</div> */}
            {/* <div className={styles.navStart}>
        <button className={styles.navStartButton}>Start</button>
      </div> */}
        </nav>
    );
}
