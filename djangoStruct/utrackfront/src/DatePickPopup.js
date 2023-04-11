import {
  DateTimePickerComponent,
  ChangeEventArgs,
} from "@syncfusion/ej2-react-calendars";
import "./Date.css";
import { format } from "date-fns";
import axios from "axios";
import { useState } from "react";

function DatePickerPopup(props) {
  let checkOutTime = null;
  let checkInTime = null;
  let facility = "1";

  const facilities = [
    { name: "Fitness Center", value: "1" },
    { name: "Aquatic Center", value: "2" },
    { name: "Racquet Center", value: "3" },
    { name: "Gymnastic Center", value: "4" },
    { name: "Bouldering Wall", value: "5" },
    { name: "Outdoor Center", value: "6" },
  ];

  const handleCheckinChange = (ChangeEventArgs) => {
    checkInTime = format(ChangeEventArgs.value, "yyyy-MM-dd'T'HH:mm:ss.SSSxxx");
  };

  const handleCheckoutChange = (ChangeEventArgs) => {
    checkOutTime = format(
      ChangeEventArgs.value,
      "yyyy-MM-dd'T'HH:mm:ss.SSSxxx"
    );
  };

  const handleSubmit = () => {
    const tracked_username = props.user.username;
    const facility_id = facility;
    if (props.disabled === false) {
      checkInTime = props.checkInTime;
    }
    axios
      .post("http://127.0.0.1:8000/api/Checkins/", {
        tracked_username,
        facility_id,
        check_in_time: checkInTime,
        check_out_time: checkOutTime,
      })
      .then((response) => {
        if (props.disabled === false) {
          axios
            .delete(
              `http://127.0.0.1:8000/api/Checkout/last/${tracked_username}/`
            )
            .then((response) => {})
            .catch((error) => {});
        }
        props.setSuccess("Request successful.");
      })
      .catch((error) => {
        props.setFailure("Invalid entry. Try again.");
      });
    props.handleClose();
  };

  return (
    <div>
      {props.disabled && (
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
        </div>
      )}
      <div style={{ display: "flex", flexDirection: "column" }}>
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

      <div style={{ display: "flex", flexDirection: "column" }}>
        <label>Facility:</label>
        <select
          onChange={(event) => {
            facility = event.target.value;
          }}
          style={{
            width: "135px",
            margin: "0 auto",
            marginTop: "10px",
          }}
        >
          <option value="1">Fitness Center</option>
          <option value="2">Aquatic Center</option>
          <option value="3">Racquet Center</option>
          <option value="4">Gymnastic Center</option>
          <option value="5">Bouldering Wall</option>
          <option value="6">Outdoor Center</option>
        </select>
      </div>

      <button
        style={{
          width: "60px",
          margin: "10px",
        }}
        onClick={props.handleClose}
      >
        Back
      </button>
      <button
        onClick={handleSubmit}
        style={{
          width: "60px",
          margin: "10px",
        }}
      >
        Submit
      </button>
    </div>
  );
}

export default DatePickerPopup;
