import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Tableau from '../components/tableau'
import NormalResults from "../components/normalResults";
import GoalResults from "../components/goalResults";
import "./result.css";

const SimplexResult = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const receivedState = location.state || {};
  let { status, optimalValue, xValues, tableaux, problemType } = receivedState;
  const finalTableau = tableaux && tableaux.length > 0 ? tableaux[tableaux.length - 1] : null;

  useEffect(() => {
    console.log("Received State in SimplexResult:", receivedState);
  }, [receivedState]);

  if (!xValues) {
    xValues = []; 
  }

  if (optimalValue === undefined || optimalValue === null) {
    optimalValue = "none"; 
  }

  if (!tableaux) {
    tableaux = []; // empty array for tableaux
  }

  const variableNames = finalTableau.columns.slice(0, xValues.length);

  return (

    <div className="container">
      <div className="content-box">
        <h2 className="title">
          {problemType === "goal" ? "Goal Programming Results" : "Simplex Method Results"}
        </h2>

        {problemType === "normal" ? (
          <NormalResults
            optimalValue={optimalValue}
            status={status}
            xValues={xValues}
            variableNames={variableNames}
          />
        ) : (
          <GoalResults
            optimalValue={optimalValue}
            xValues={xValues}
          />
        )}

        <div>
          {tableaux.map((tableau, stepIndex) => (
            <div key={stepIndex}>
              <p className="tableau-title">Tableau Step {stepIndex + 1}</p>
              <Tableau tableau={tableau} />
            </div>
          ))}
        </div>


        <div className="button-container">
          <button onClick={() => navigate("/")} className="back-button">
            Back to Main Page
          </button>
        </div>
      </div>
    </div>
  );
};

export default SimplexResult;
