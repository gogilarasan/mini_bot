import axios from 'axios'; // Import axios

const API_BASE_URL = 'http://127.0.0.1:5000/api';

const DocumentAnalyzer = {
  uploadDocument: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading document:', error);
      throw error;
    }
  },

  askQuestion: async (context, question) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/ask`, { context, question });
      return response.data.answer;
    } catch (error) {
      console.error('Error asking question:', error);
      throw error;
    }
  }
};

export default DocumentAnalyzer;
