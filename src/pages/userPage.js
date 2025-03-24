import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

const LinearProgrammingSolver = () => {
  const [problemType, setProblemType] = useState("normal"); // Normal or Goal Programming
  const [numVariables, setNumVariables] = useState();
  const [numEquations, setNumEquations] = useState();
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
  const [isLoading, setIsLoading] = useState(false); // Loading state

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
      setIsLoading(true); // Start loading
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
      console.log("Server Response:janjoon", responseData);
  
      // Save state to localStorage
      const stateData = {
        problemType,
        numVariables,
        numEquations,
        numGoals,
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
      localStorage.setItem("linearProgrammingState", JSON.stringify(stateData));
  
      setTimeout(() => {
        setIsLoading(false); // Stop loading
        navigate("/simplex-result", { 
          state: {
            status:responseData.status,
            optimalValue: responseData.optimalZ,
            xValues: responseData.xValues,
            tableaux: responseData.tableau, // Last tableau step
            problemType: problemType
          }
        });
      }, 2000); // 1 second delay
  
    } catch (error) {
      console.error("Error sending data:", error);
    }
  };


    // Load state from localStorage when the component mounts
    useEffect(() => {
      const savedState = localStorage.getItem("linearProgrammingState");
      if (savedState) {
        const parsedState = JSON.parse(savedState);
        setProblemType(parsedState.problemType);
        setNumVariables(parsedState.numVariables);
        setNumEquations(parsedState.numEquations);
        setNumGoals(parsedState.numGoals);
        setObjectiveCoefficients(parsedState.objectiveCoefficients);
        setObjectiveType(parsedState.objectiveType);
        setTechnique(parsedState.technique);
        setConstraints(parsedState.constraints);
        setGoals(parsedState.goals);
        setUnrestrictedVariables(parsedState.unrestrictedVariables);
        setGoalPriorityType(parsedState.goalPriorityType);
        setGoalPriorities(parsedState.goalPriorities);
        setGoalWeights(parsedState.goalWeights);
      }
    }, []);
  

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

  const handleReload = () => {
    localStorage.clear(); // Clears all localStorage data
    window.location.reload(); // Reloads the page
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
        <select 
        value = {problemType}
        onChange={(e) => setProblemType(e.target.value)}>
          <option value="normal">Normal Min/Max Problem</option>
          <option value="goal">Goal Programming</option>
        </select>

        {(problemType === "normal") && (
          <select onChange={(e) => setTechnique(e.target.value)}
          value={technique}>
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
            value={numVariables}
          />
          <input
            type="number"
            placeholder="Number of Constraints"
            onChange={(e) => setNumEquations(Number(e.target.value))}
            value={numEquations}
          />
          {problemType === "goal" && (
            <input
              type="number"
              placeholder="Number of Goals"
              onChange={(e) => setNumGoals(Number(e.target.value))}
              value={numGoals}
            />
          )}
        </div>
      )}

{(problemType === "normal") && (
     <div>
     <h2>Objective Function</h2>
     <div>
       <select onChange={(e) => setObjectiveType(e.target.value)}
                value={objectiveType}>
         <option value="max">Maximize</option>
         <option value="min">Minimize</option>
       </select>
       <span> Z = </span>
       {Array.from({ length: numVariables }).map((_, index) => (
         <input
           key={index}
           type="text"
           placeholder={`x${index + 1}`}
           value={objectiveCoefficients[index] || ''} // Set the value from constraints
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
                value={constraints[eqIndex]?.coefficients[varIndex] || ''} // Set the value from constraints
                placeholder={`x${varIndex + 1}`}
                onChange={(e) => handleEquationChange(eqIndex, varIndex, e.target.value, constraints, setConstraints)}
              />
            ))}
            <select onChange={(e) => handleEquationChange(eqIndex, "operator", e.target.value, constraints, setConstraints)}
                    value={constraints[eqIndex]?.operator || '='} // Set the operator value
>
              <option value="<=">≤</option>
              <option value=">=">≥</option>
              <option value="=">=</option>
            </select>
            <input
              type="text"
              placeholder="RHS"
              value={constraints[eqIndex]?.rhs || ''} // Set the value from constraints
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
                  value={goals[goalIndex]?.coefficients[varIndex] || ''} // Set the value from constraints
                  onChange={(e) => handleEquationChange(goalIndex, varIndex, e.target.value, goals, setGoals)}
                />
              ))}
              <select onChange={(e) => handleEquationChange(goalIndex, "operator", e.target.value, goals, setGoals)}
                  value={goals[goalIndex]?.operator || '='}> // Set the operator value

                <option value="<=">≤</option>
                <option value=">=">≥</option>
                <option value="=">=</option>
              </select>
              <input
                type="text"
                placeholder="RHS"
                value={goals[goalIndex]?.rhs || ''} // Set the value from constraints
                onChange={(e) => handleEquationChange(goalIndex, "rhs", e.target.value, goals, setGoals)}
              />
            </div>
          ))}
          
          <h2>Goal Prioritization</h2>
          
          {problemType === "goal" && (
  <div>
    {Array.from({ length: numGoals }).map((_, goalIndex) => (
      <React.Fragment key={goalIndex}>
        <input
          type="number"
          min="1"
          max={numGoals}
          placeholder={`Priority for Goal ${goalIndex + 1}`}
          onChange={(e) => {
            const updatedPriorities = [...goalPriorities];
            updatedPriorities[goalIndex] = e.target.value;
            setGoalPriorities(updatedPriorities);

            // Convert to integers like [3,1,2]
            const extracted = updatedPriorities.map((val) =>
              val ? parseInt(val) : null
            );

            // Create array of priorities: goal i has rank X
            const goalRanks = Array(numGoals).fill(0);
            extracted.forEach((goalNumber, inputIndex) => {
              if (goalNumber && goalNumber >= 1 && goalNumber <= numGoals) {
                goalRanks[goalNumber - 1] = inputIndex + 1;
              }
            });

            setGoalPriorities(goalRanks);
          }}
        />
        {goalIndex < numGoals - 1 && (
          <span style={{ margin: "0 10px" }}> &gt; </span>
        )}
      </React.Fragment>
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
                checked={unrestrictedVariables.includes(index.toString())} // Check if the variable is in the unrestrictedVariables array
              />
              {` x${index + 1}`}
            </label>
          ))}
        </div>
      )}
      
      <button onClick={sendDataToServer} style={{ width: "100%", marginTop: "10px", padding: "10px", backgroundColor: "blue", color: "white", border: "none", cursor: "pointer" }}>Solve</button>
      <button onClick={handleReload} style={{ width: "100%", marginTop: "10px", padding: "10px", backgroundColor: "white", color: "black", border: "none", cursor: "pointer" }}>clear Inputs</button>

      {isLoading && (
        <div className="loading-overlay">
<div class="loader"></div>
  <p>Hang tight! We're almost there...</p>
</div>

      )}
    </div>
  );
};

export default LinearProgrammingSolver;
