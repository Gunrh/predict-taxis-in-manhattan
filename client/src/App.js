import React from "react";
import ReactNYC from "react-nyc-choropleth";
import "./app.css";

const App = (props) => {
  const mapboxAccessToken =
    "pk.eyJ1IjoiYmFya2FydGExIiwiYSI6ImNsMTI2ZXh6NzAwMHIzb210am5xenN2dTUifQ.7otIOgSNLp8uAdGFTdRpOw"; // Your access token
  const mapboxType = "streets";
  const position = [40.7831, -73.9712];
  const zoom = 12;

  const data = props.data;
  const neighborhoodStyle = {
    weight: 1,
    opacity: 1,
    color: "#121212",
    dashArray: "3",
    fillOpacity: 0.7,
  };
  const neighborhoodHoverStyle = {
    weight: 5,
    color: "#ff8c00",
    dashArray: "1",
    fillOpacity: 0.7,
  };
  const excludeNeighborhoods = [];

  return (
    <div className="outer-map-container">
      <ReactNYC
        mapboxAccessToken={mapboxAccessToken} // Required
        mapHeight="100%" // Required
        mapWidth=""
        className="container"
        mapboxType="dark"
        mapCenter={position}
        mapZoom={zoom}
        mapScrollZoom={false}
        neighborhoodOn={true}
        tooltip={true}
        tooltipSticky={false}
        data={data}
        neighborhoodStyle={neighborhoodStyle}
        neighborhoodHoverStyle={neighborhoodHoverStyle}
        excludeNeighborhoods={excludeNeighborhoods}
      />
    </div>
  );
};

export default App;
