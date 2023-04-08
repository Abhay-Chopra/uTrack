import React, { useState } from "react";
import {
  DateTimePickerComponent,
  ChangeEventArgs,
} from "@syncfusion/ej2-react-calendars";
import "./Date.css";
import { format } from "date-fns";
import axios from "axios";

function DatePickerPopup(props) {
  const [tracked_username, setTrackedUsername] = useState("");
  const [facility_id, setFacilityId] = useState("");
  let check_in_time = "";
  let check_out_time = null;

  const handleCheckinChange = (ChangeEventArgs) => {
    check_in_time = format(
      ChangeEventArgs.value,
      "yyyy-MM-dd'T'HH:mm:ss.SSSxxx"
    );
  };

  const handleCheckoutChange = (ChangeEventArgs) => {
    check_out_time = format(
      ChangeEventArgs.value,
      "yyyy-MM-dd'T'HH:mm:ss.SSSxxx"
    );
  };

  const handleSubmit = () => {
    setTrackedUsername(props.user.username);
    setFacilityId("1");
    axios
      .post("http://127.0.0.1:8000/api/Checkins/", {
        tracked_username,
        facility_id,
        check_in_time,
        check_out_time,
      })
      .then((response) => {})
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <label>Check-in Time:</label>
        <DateTimePickerComponent
          placeholder="Choose the date and time this user came in."
          step={10}
          change={handleCheckinChange}
          style={{
            color: "white",
          }}
        />
        <label>Check-out Time:</label>
        <DateTimePickerComponent
          placeholder="Choose the date and time this user left."
          step={10}
          change={handleCheckoutChange}
          style={{
            color: "white",
          }}
        />
      </div>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default DatePickerPopup;
