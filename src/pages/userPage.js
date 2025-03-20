import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

const LinearProgrammingSolver = () => {
  const [problemType, setProblemType] = useState("normal"); // Normal or Goal Programming
  const [numVariables, setNumVariables] = useState(0);
  const [numEquations, setNumEquations] = useState(0);
  const [numGoals, setNumGoals] = useState(0);
  const [objectiveCoefficients, setObjectiveCoefficients] = useState([]);
  const [objectiveType, setObjectiveType] = useState("max");
  const [technique, setTechnique] = useState("bigm");
  const [constraints, setConstraints] = useState([]);
  const [goals, setGoals] = useState([]);
  const [unrestrictedVariables, setUnrestrictedVariables] = useState([]);
  const [goalPriorityType, setGoalPriorityType] = useState("weights"); // Weights or Priorities
  const [goalPriorities, setGoalPriorities] = useState([]);
  const [goalWeights, setGoalWeights] = useState([]);
  const navigate = useNavigate();


  const sendDataToServer = async () => {
    const requestData = {
      problemType,
      objectiveCoefficients,
      objectiveType,
      technique,
      constraints,
      goals,
      unrestrictedVariables,
      goalPriorityType,
      goalPriorities,
      goalWeights
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/process-data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        throw new Error("Failed to send data");
      }

      const responseData = await response.json();
      console.log("Server Response:zzzzzzzzzzz", responseData);

      navigate("/simplex-result", { state: {
        optimalValue: responseData.optimalZ,
        xValues: responseData.xValues,
        tableaux: responseData.tableau // Last tableau step
      }});

    } catch (error) {
      console.error("Error sending data:", error);
    }
  };

  const handleVariableChange = (index, value) => {
    let updatedCoefficients = [...objectiveCoefficients];
    updatedCoefficients[index] = value;
    setObjectiveCoefficients(updatedCoefficients);
  };
  const handleUnrestrictedChange = (value) => {
    setUnrestrictedVariables((prev) => {
      const updated = prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value];
      return updated;
    });
  };
  

  const initializeConstraintIfNeeded = (eqIndex, targetArray) => {
    let updatedArray = [...targetArray];
    if (!updatedArray[eqIndex]) {
      updatedArray[eqIndex] = { coefficients: Array(numVariables).fill(""), operator: "<=", rhs: "" };
    }
    return updatedArray;
  };

  const handleEquationChange = (eqIndex, key, value, targetArray, setter) => {
    let updatedArray = initializeConstraintIfNeeded(eqIndex, targetArray);
  
    if (key === "operator" || key === "rhs") {
      // Update the operator or RHS directly in the constraint object
      updatedArray[eqIndex][key] = value;
    } else {
      // Otherwise, assume it's a coefficient and update normally
      updatedArray[eqIndex].coefficients[key] = value;
    }
  
    setter([...updatedArray]); // Ensure re-render by spreading the array
  };
  

  return (
    <div style={{ padding: "20px", margin: "auto", textAlign: "center" }}>
      <h1>Linear Programming Solver</h1>
      
      <div>
        <label>Select Problem Type: </label>
        <select onChange={(e) => setProblemType(e.target.value)}>
          <option value="normal">Normal Min/Max Problem</option>
          <option value="goal">Goal Programming</option>
        </select>

        {(problemType === "normal") && (
          <select onChange={(e) => setTechnique(e.target.value)}>
         <option value="bigm">Big M</option>
         <option value="twophase">Two-Phase</option>
       </select>
      )}
      </div>
      
      {(problemType === "normal" || problemType === "goal") && (
        <div>
          <input
            type="number"
            placeholder="Number of Variables"
            onChange={(e) => setNumVariables(Number(e.target.value))}
          />
          <input
            type="number"
            placeholder="Number of Constraints"
            onChange={(e) => setNumEquations(Number(e.target.value))}
          />
          {problemType === "goal" && (
            <input
              type="number"
              placeholder="Number of Goals"
              onChange={(e) => setNumGoals(Number(e.target.value))}
            />
          )}
        </div>
      )}

{(problemType === "normal") && (
     <div>
     <h2>Objective Function</h2>
     <div>
       <select onChange={(e) => setObjectiveType(e.target.value)}>
         <option value="max">Maximize</option>
         <option value="min">Minimize</option>
       </select>
       <span> Z = </span>
       {Array.from({ length: numVariables }).map((_, index) => (
         <input
           key={index}
           type="text"
           placeholder={`x${index + 1}`}
           onChange={(e) => handleVariableChange(index, e.target.value)}
         />
       ))}

     </div>
   </div>
      )}
      
      <div>
        <h2>Constraints</h2>
        {Array.from({ length: numEquations }).map((_, eqIndex) => (
          <div key={eqIndex}>
            {Array.from({ length: numVariables }).map((_, varIndex) => (
              <input
                key={varIndex}
                type="text"
                placeholder={`x${varIndex + 1}`}
                onChange={(e) => handleEquationChange(eqIndex, varIndex, e.target.value, constraints, setConstraints)}
              />
            ))}
            <select onChange={(e) => handleEquationChange(eqIndex, "operator", e.target.value, constraints, setConstraints)}>
              <option value="<=">≤</option>
              <option value=">=">≥</option>
              <option value="=">=</option>
            </select>
            <input
              type="text"
              placeholder="RHS"
              onChange={(e) => handleEquationChange(eqIndex, "rhs", e.target.value, constraints, setConstraints)}
            />
          </div>
        ))}
      </div>
      
      {problemType === "goal" && numGoals > 0 && (
        <div>
          <h2>Goal Equations</h2>
          {Array.from({ length: numGoals }).map((_, goalIndex) => (
            <div key={goalIndex}>
              {Array.from({ length: numVariables }).map((_, varIndex) => (
                <input
                  key={varIndex}
                  type="text"
                  placeholder={`x${varIndex + 1}`}
                  onChange={(e) => handleEquationChange(goalIndex, varIndex, e.target.value, goals, setGoals)}
                />
              ))}
              <select onChange={(e) => handleEquationChange(goalIndex, "operator", e.target.value, goals, setGoals)}>
                <option value="<=">≤</option>
                <option value=">=">≥</option>
                <option value="=">=</option>
              </select>
              <input
                type="text"
                placeholder="RHS"
                onChange={(e) => handleEquationChange(goalIndex, "rhs", e.target.value, goals, setGoals)}
              />
            </div>
          ))}
          
          <h2>Goal Prioritization</h2>
          <label>
            <input
              type="radio"
              value="weights"
              checked={goalPriorityType === "weights"}
              onChange={() => setGoalPriorityType("weights")}
            />
            Weights
          </label>
          <label>
            <input
              type="radio"
              value="priorities"
              checked={goalPriorityType === "priorities"}
              onChange={() => setGoalPriorityType("priorities")}
            />
            Priorities
          </label>
          
          {goalPriorityType === "weights" && (
            <div>
              <h3>Assign Weights</h3>
              {Array.from({ length: numGoals }).map((_, goalIndex) => (
                <input
                  key={goalIndex}
                  type="number"
                  placeholder={`Weight for Goal ${goalIndex + 1}`}
                  onChange={(e) => {
                    let updatedWeights = [...goalWeights];
                    updatedWeights[goalIndex] = e.target.value;
                    setGoalWeights(updatedWeights);
                  }}
                />
              ))}
            </div>
          )}
          
          {goalPriorityType === "priorities" && (
            <div>
              <h3>Set Priorities</h3>
              {Array.from({ length: numGoals }).map((_, goalIndex) => (
                <input
                  key={goalIndex}
                  type="text"
                  placeholder={`Priority for Goal ${goalIndex + 1} (e.g. p${goalIndex + 1})`}
                  onChange={(e) => {
                    let updatedPriorities = [...goalPriorities];
                    updatedPriorities[goalIndex] = e.target.value;
                    setGoalPriorities(updatedPriorities);

                  }}
                />
              ))}
            </div>
          )}
        </div>
      )}

{numVariables > 0 && (
        <div>
          <h2>Select Unrestricted Variables</h2>
          {Array.from({ length: numVariables }).map((_, index) => (
            <label key={index} style={{ marginRight: "10px" }}>
              <input
                type="checkbox"
                value={index}
                onChange={(e) => handleUnrestrictedChange(e.target.value)}
              />
              {` x${index + 1}`}
            </label>
          ))}
        </div>
      )}
      
      <button onClick={sendDataToServer} style={{ width: "100%", marginTop: "10px", padding: "10px", backgroundColor: "blue", color: "white", border: "none", cursor: "pointer" }}>Solve</button>
    </div>
  );
};

export default LinearProgrammingSolver;
