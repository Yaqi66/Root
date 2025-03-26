import styles from '../styles/page.module.css';

export default function TextContainer({ title, subtitle }) {
    return (
        <div className={styles.textContainer}>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    );
}
