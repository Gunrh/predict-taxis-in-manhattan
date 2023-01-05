import { useState } from "react";
import App from "./App";
import Input_Row from "./Input_Row";
import "./main_comp.css";

const Main_comp = () => {
  const [data, setData] = useState([]);

  return (
    <div className="container">
      <div className="title">
        <h1>New York City - Taxi Prediction Demo</h1>
      </div>
      <div className="contentContainer">
        <div className="leftContainer">
          <Input_Row set_data={setData} />
        </div>
        <div className="rightContainer">
          <App data={data} />
        </div>
      </div>
    </div>
  );
};
export default Main_comp;
