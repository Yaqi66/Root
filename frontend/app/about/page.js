'use client';

import Navbar from '../ui/components/Navbar';
import ActionButton from '../ui/components/ActionButton';
import styles from '../ui/styles/page.module.css';
import additionalStyles from '../ui/styles/about.module.css';

export default function About() {
    return (
        <div className={styles.page}>
            <main className={styles.main}>
                <Navbar />
                <div className={styles.content}>
                    <div className={additionalStyles.textContainer}>
                        <h1>About ROOT</h1>
                        <p>
                            ROOT is a plant monitoring system that uses a
                            Raspberry Pi equipped with environmental sensors and
                            a camera to track plant health and growth. The
                            sensors measure key environmental factors such as
                            dew point, pH, and temperature, while the camera
                            captures images of the plant.
                        </p>
                        <p>
                            All data is streamed to Azure for real-time
                            processing and visualization. Azure Custom Vision
                            helps classify plant types and estimate growth,
                            enhancing insights into plant health. Additional
                            Azure services manage data storage, analytics, and
                            visualization.
                        </p>
                    </div>
                    <div
                        className={`${styles.actionButtonContainer} ${additionalStyles.actionButtonContainer}`}
                    >
                        <ActionButton text="Home" type="primary" route="/" />
                    </div>
                    <p>Project by Yaqi and Yaroslav.</p>
                </div>
            </main>
        </div>
    );
}
