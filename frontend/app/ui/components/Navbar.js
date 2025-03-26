import Image from 'next/image';
import styles from '../styles/page.module.css';

export default function Navbar() {
    return (
        <nav className={styles.navBar}>
            <div className={styles.navLogo}>
                <Image
                    src={'/pictures/logoLight.png'}
                    alt="Logo"
                    width={200}
                    height={80}
                />
            </div>
            {/* Optional dock or buttons if needed */}
            {/* <div className={styles.navDock}>Dock</div> */}
            {/* <div className={styles.navStart}>
        <button className={styles.navStartButton}>Start</button>
      </div> */}
        </nav>
    );
}
