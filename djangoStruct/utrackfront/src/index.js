import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { registerLicense } from "@syncfusion/ej2-base";
import reportWebVitals from "./reportWebVitals";

registerLicense(
  "Mgo+DSMBaFt+QHFqVk5rWU5DaV1CX2BZf1l2QmlYe04QCV5EYF5SRHJfRVxgTH9Rd0JmW3o=;Mgo+DSMBPh8sVXJ1S0d+X1lPc0BFQmFJfFBmRGlZeFRxcEUmHVdTRHRcQlljTn9Qc0RhWHhYd3E=;ORg4AjUWIQA/Gnt2VFhhQlJMfVpdWnxLflF1VWJTf1l6dVFWACFaRnZdQV1nSXlSdUBiW35ZeHZQ;MTY1MzI1NEAzMjMxMmUzMTJlMzMzOGc3ZEk4NG9uVm1aUlh0eGsyelZpMW5LUGRRT2ZwNWpJOURHWERkejFRM289;MTY1MzI1NUAzMjMxMmUzMTJlMzMzOGxGTFRIaWZlOC9TZExHTlVBa09GTDl0MC8rY21yOTRUckRrK0VGRFBsOGs9;NRAiBiAaIQQuGjN/V0d+XU9HflRHQmRWfFN0RnNYdV53flRCcDwsT3RfQF5jTX5Ud0ZmWH1feHBQQw==;MTY1MzI1N0AzMjMxMmUzMTJlMzMzOFpTSjRhaUJZSVNZRTUrOEkrTXhvRHd6MmVDUUtpRkdBbDJIUVlBZ2gwQnc9;MTY1MzI1OEAzMjMxMmUzMTJlMzMzOFI5bmdtd2YxNnRndk11MmgxSG80MlU1SnBVaC9RZFJGaVZ0eHh6YjZlM0k9;Mgo+DSMBMAY9C3t2VFhhQlJMfVpdWnxLflF1VWJTf1l6dVFWACFaRnZdQV1nSXlSdUBiW35XcHxQ;MTY1MzI2MEAzMjMxMmUzMTJlMzMzOEU1TU9Ha2RJWVZBOHZIRlJqaHFZWUt4cjliYjNmZGRCVWxSdXZ2MUFkcjg9;MTY1MzI2MUAzMjMxMmUzMTJlMzMzOFk4cFlDdHZJaVF2dTBzeU5SYmk1UjNiT2FPQnBWRXZNZ21KaURMUW5aV1k9;MTY1MzI2MkAzMjMxMmUzMTJlMzMzOFpTSjRhaUJZSVNZRTUrOEkrTXhvRHd6MmVDUUtpRkdBbDJIUVlBZ2gwQnc9"
);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
