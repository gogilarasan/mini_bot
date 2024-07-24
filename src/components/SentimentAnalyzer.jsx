import { analyzeSentiment } from '../services/api';

const SentimentAnalyzer = async (text) => {
    return await analyzeSentiment(text);
};

export default SentimentAnalyzer;
