import axios from "axios";
import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Moment from "moment";
import Multiselect from "multiselect-react-dropdown";
import "./input_rows.css";

const Input_Row = (props) => {
  const [zone, setZone] = useState([]);
  const [date, setDate] = useState(new Date());

  const handleSubmit = (event) => {
    event.preventDefault();
    if (zone == [] || date == "") {
      alert("Must Fill all Inputs");
      return;
    }
    axios({
      method: "post",
      url: "http://localhost:5000/calc",
      headers: { "Content-Type": "application/json" },
      data: {
        zone: zone,
        date: Moment(date).format("DD/MM/yyyy"),
        time: Moment(date).format("HH:mm"),
      },
    })
      .then((res) => {
        console.log(res);
        props.set_data(res.data);
      })
      .catch((res) => {
        console.log(res);
      });
  };
  const selected_zones = (e) => {
    setZone(e);
    let data = [];
    e.forEach((item) => {
      data.push({
        name: item,
        color: "#ed5f00",
      });
    });
    props.set_data(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input_rows">
        <div>
          <label for="zone">Zone:</label>
          <Multiselect
            isObject={false}
            onKeyPressFn={function noRefCheck() {}}
            onRemove={selected_zones}
            onSearch={function noRefCheck() {}}
            onSelect={selected_zones}
            options={[
              "Inwood",
              "Washington Heights",
              "Hamilton Heights",
              "Central Harlem",
              "Morningside Heights",
              "Upper West Side",
              "Central Park",
              "Spanish Harlem",
              "Randall's Island",
              "Upper East Side",
              "Roosevelt Island",
              "Midtown West",
              "Midtown East",
              "Kips Bay",
              "Stuyvesant Town",
              "Chelsea",
              "Flatiron District",
              "West Village",
              "Greenwich Village",
              "East Village",
              "Soho",
              "Lower East Side",
              "Tribeca",
              "Two Bridges",
              "Battery Park City",
              "Financial District",
            ]}
          />
        </div>

        <div className="datePickerStyle">
          <label for="Date & Time">Date & Time:</label>
          <DatePicker
            selected={date}
            onChange={(date) => setDate(date)}
            timeInputLabel="Time:"
            dateFormat="MM/dd/yyyy h:mm aa"
            showTimeInput
          />
        </div>
        <input className="submitButton" type="submit" value="Submit" />
      </div>
    </form>
  );
};
export default Input_Row;
