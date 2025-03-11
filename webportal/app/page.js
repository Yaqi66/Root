'use client'

import Image from "next/image"
import logoL from "./ui/pictures/logoLight.png"
import logoD from "./ui/pictures/logoDark.png"
import logoAlt from "./ui/pictures/logoAlternative.png"
import styles from "./ui/page.module.css";

export default function Home() {

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <nav className={styles.navBar}>
          <div className={styles.navLogo}>
            {/*  for Alt */}
            <Image src={logoAlt} alt="Logo" width={100} height={80} />

            {/* for light or dark */}
            {/* <Image src={logoL} alt="Logo" width={200} height={80} /> */}
          </div>
          <div className={styles.navDock}>
            Dock
          </div>
          <div className={styles.navStart}>
            <button className={styles.navStartButton}>Start</button>
          </div>
        </nav>
        <div className={styles.content}>
          <div className={styles.textContainer}>
            <h1>ROOT</h1>
            <p>care for your plant</p>
          </div>
          <div className={styles.actionButtonContainer}>
            <button className={`${styles.button} ${styles.startButton}`}>Start</button>
            <button className={`${styles.button} ${styles.aboutButton}`}>About</button>
          </div>
        </div>
      </main>
    </div>
  );
}
