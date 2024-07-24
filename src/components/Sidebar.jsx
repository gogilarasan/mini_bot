import React from "react";
import {
  AiOutlineFile,
  AiOutlineSmile,
  AiOutlineSetting,
  AiOutlineHome,
  AiOutlineInfoCircle,
} from "react-icons/ai";
import "../styles/Sidebar.css";

const Sidebar = ({ setMode, setDetailLevel, setTheme }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>Chat App</h1>
        <button
          className="settings-button"
          onClick={() => setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"))}
        >
          <AiOutlineSetting className="icon" />
          Toggle Theme
        </button>
      </div>
      <div className="sidebar-menu">
        <button className="menu-item" onClick={() => setMode("sentiment")}>
          <AiOutlineSmile className="icon" />
          Sentiment Analysis
        </button>
        <button className="menu-item" onClick={() => setMode("document")}>
          <AiOutlineFile className="icon" />
          Document Analysis
        </button>
      </div>
      <div className="sidebar-footer">
        <select
          onChange={(e) => setDetailLevel(e.target.value)}
          className="summary-select"
        >
          <option value="brief">Brief Summary</option>
          <option value="detailed">Detailed Summary</option>
        </select>
        <div className="footer-icons">
          <AiOutlineHome className="icon" />
          <AiOutlineInfoCircle className="icon" />
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
