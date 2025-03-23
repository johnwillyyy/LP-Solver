import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./result.css";

const SimplexResult = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const receivedState = location.state || {};
  let { optimalValue, xValues, tableaux, problemType } = receivedState;
  const finalTableau = tableaux && tableaux.length > 0 ? tableaux[tableaux.length - 1] : null;

  useEffect(() => {
    console.log("Received State in SimplexResult:", receivedState);
  }, [receivedState]);

  if (!xValues) {
    xValues = []; // empty array for xValues
  }

  if (optimalValue === undefined || optimalValue === null) {
    optimalValue = "none"; // default to "none" if optimalValue is null or undefined
  }

  if (!tableaux) {
    tableaux = []; // empty array for tableaux
  }
  console.log(xValues);
  console.log(optimalValue);
  const variableNames = finalTableau.columns.slice(0, xValues.length);

  return (
    <div className="container">
      <div className="content-box">
        <h2 className="title">
          {problemType === "goal" ? "Goal Programming Results" : "Simplex Method Results"}
        </h2>

        {problemType === "normal" ? (
          <>
            <div className="optimal-value">
              Optimal Value: <span className="optimal-value-text">{optimalValue}</span>
            </div>

            <div className="solution-box">
              <p className="solution-title">Solution (X Values):</p>
              <div className="solution-values">
                {xValues.map((val, index) => (
                  <span key={index} className="solution-item">
                    {problemType === "normal"
                      ? `${variableNames[index]} = ${val.toFixed(2)}`
                      : `x${index + 1} = ${parseFloat(val).toFixed(2)}`}
                  </span>
                ))}
              </div>
            </div>
          </>
        ) : (
          <>
            <div className="goal-status-box">
              <p className="solution-title">Goal Status:</p>
              <div className="goal-status-values">
              {optimalValue.map(([goalName, status], index) => (
  <div key={index} className="goal-status-item">
    <strong>{goalName}</strong>:{" "}
    <span
      className={
        status === "Satisfied"
          ? "status-satisfied"
          : "status-unsatisfied"
      }
                    >
                      {status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="solution-box">
              <p className="solution-title">Variable Values:</p>
              <div className="solution-values">
                {xValues.map((val, index) => (
                  <span key={index} className="solution-item">
                    {`x${index + 1} = ${parseFloat(val).toFixed(2)}`}
                  </span>
                ))}
              </div>
            </div>
          </>
        )}

        {tableaux.map((tableau, stepIndex) => (
          <div key={stepIndex} className="tableau-container">
            <p className="tableau-title">Tableau Step {stepIndex + 1}</p>
            <div className="tableau-wrapper">
              <table className="tableau">
                <thead>
                  <tr className="tableau-header">
                    <th className="tableau-cell">Basis</th>
                    {tableau.columns.map((col, index) => (
                      <th key={index} className="tableau-cell">{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {tableau.tableau.map((row, rowIndex) => (
                    <tr key={rowIndex} className="tableau-row">
                      <td className="tableau-cell basis-cell">
                        {tableau.rows[rowIndex]}
                      </td>
                      {row.map((cell, colIndex) => (
                        <td key={colIndex} className="tableau-cell">
                          {parseFloat(cell).toFixed(2)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}

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
