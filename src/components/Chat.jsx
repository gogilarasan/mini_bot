import React, { useState } from "react";
import ChatMessage from "./ChatMessage";
import SentimentAnalyzer from "./SentimentAnalyzer";
import DocumentAnalyzer from "./DocumentAnalyzer";
import Sidebar from "./Sidebar";
import "../styles/Chat.css";
import {
  AiOutlineFile,
  AiOutlineSend,
  AiOutlineQuestionCircle,
  AiOutlineUpload,
} from "react-icons/ai";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [uploadInfo, setUploadInfo] = useState({ summary: "", text: "" });
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [mode, setMode] = useState("sentiment");
  const [detailLevel, setDetailLevel] = useState("brief");
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState("light"); // New state for theme

  const handleSend = async () => {
    if (input.trim()) {
      const newMessage = { text: input, sender: "user" };
      setMessages([...messages, newMessage]);
  
      setLoading(true);
      try {
        if (mode === "sentiment") {
          const analysis = await SentimentAnalyzer(input);
          console.log("Sentiment Analysis Response:", analysis); // Log the response
          const botMessage = {
            text: `Sentiment Analysis: ${JSON.stringify(analysis)}`,
            sender: "bot",
          };
          setMessages((prevMessages) => [...prevMessages, botMessage]);
        } else if (mode === "document" && uploadInfo.text) {
          const data = await DocumentAnalyzer.askQuestion(uploadInfo.text, input);
          console.log("Document Analysis Response:", data); // Log the response
          
          const botMessage = {
            text: `Answer: ${data}`,
            sender: "bot",
          };
          setMessages((prevMessages) => [...prevMessages, botMessage]);
        }
      } catch (error) {
        console.error("Error during processing:", error);
        const errorMessage = {
          text: "An error occurred. Please try again.",
          sender: "bot",
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }
      setLoading(false);
      setInput("");
    }
  };  

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (file) {
      setLoading(true);
      try {
        const data = await DocumentAnalyzer.uploadDocument(file, detailLevel);
        setUploadInfo({ summary: data.summary, text: data.text });
        setQuestion("");
        setAnswer("");
      } catch (error) {
        console.error("Error uploading document:", error);
        setUploadInfo({ summary: "Error uploading document.", text: "" });
      }
      setLoading(false);
    }
  };

  return (
    <div className={`chat-container ${theme}`}>
      <Sidebar
        setMode={setMode}
        setDetailLevel={setDetailLevel}
        setTheme={setTheme}
      />
      <div className="chat-content">
        <div className="chat-box">
          {messages.map((msg, index) => (
            <ChatMessage key={index} message={msg} />
          ))}
          {uploadInfo.summary && (
            <div className="upload-info">
              <strong>Summary:</strong> {uploadInfo.summary}
            </div>
          )}
          {answer && (
            <div className="upload-info">
              <strong>Answer:</strong> {answer}
            </div>
          )}
          {loading && <div className="loading">Loading...</div>}
        </div>
        <div className="chat-controls">
          {mode === "document" && (
            <>
              <div className="file-upload-container">
                <input type="file" onChange={handleFileChange} />
                <button onClick={handleUpload} className="upload-button">
                  <AiOutlineUpload /> Upload Document
                </button>
              </div>
            </>
          )}
          <div className="chat-input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={
                mode === "sentiment" ? "Type a message..." : "Ask a question..."
              }
              className="chat-input"
            />
            <button onClick={handleSend} className="send-button">
              <AiOutlineSend /> Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
