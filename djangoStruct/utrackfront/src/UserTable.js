import React, { useState, useEffect } from "react";
import axios from "axios";
import DatePickPopup from "./DatePickPopup";
import { useHistory, useLocation } from "react-router-dom";

function UserTable() {
  let userName = "";
  const [sessions, setSessions] = useState([]);
  const location = useLocation();
  userName = location.state.params;

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/Checkins/?tracked_username=30143943")
      .then((response) => {
        setSessions(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div style={{ height: "400px", overflow: "scroll" }}>
      <h2>
        <span>User: </span>
        <span>{}</span>
      </h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Facility</th>
            <th>Hours</th>
            <th>Rentals</th>
          </tr>
        </thead>
        <tbody>
          {sessions.map((session) => (
            <tr key={session.tracked_username}>
              <td>session</td>
              <td>{session.facility_id}</td>
              <td>{session.time_in_facility}</td>
              <td>k</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={() => {}}>Add Rentals</button>
    </div>
  );
}

export default UserTable;
