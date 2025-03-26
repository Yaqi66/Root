import Navbar from './ui/components/Navbar';
import ActionButton from './ui/components/ActionButton';
import TextContainer from './ui/components/TextContainer';
import styles from './ui/styles/page.module.css';

export default function Home() {
    return (
        <div className={styles.page}>
            <main className={styles.main}>
                <Navbar />
                <div className={styles.content}>
                    <TextContainer
                        title="ROOT"
                        subtitle="care for your plant"
                    />
                    <div className={styles.actionButtonContainer}>
                        <ActionButton
                            text="Start"
                            type="primary"
                            route="/dashboard"
                        />
                        <ActionButton
                            text="About"
                            type="secondary"
                            route="/about"
                        />
                    </div>
                </div>
            </main>
        </div>
    );
}
