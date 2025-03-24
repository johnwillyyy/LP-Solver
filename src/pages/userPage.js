import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";
import ProblemFormSelector from "../components/ProblemFormSelector";
import ObjectiveFunction from "../components/ObjectiveFunction";
import ConstraintsInput from "../components/ConstraintsInput";
import GoalProgrammingSection from "../components/GoalProgrammingSection";
import UnrestrictedVariables from "../components/UnrestrictedVariables";

const LinearProgrammingSolver = () => {
  const [problemType, setProblemType] = useState("normal");
  const [numVariables, setNumVariables] = useState();
  const [numEquations, setNumEquations] = useState();
  const [numGoals, setNumGoals] = useState();
  const [objectiveCoefficients, setObjectiveCoefficients] = useState([]);
  const [objectiveType, setObjectiveType] = useState("max");
  const [technique, setTechnique] = useState("bigm");
  const [constraints, setConstraints] = useState([]);
  const [goals, setGoals] = useState([]);
  const [unrestrictedVariables, setUnrestrictedVariables] = useState([]);
  const [goalPriorities, setGoalPriorities] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

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
      setGoalPriorities(parsedState.goalPriorities);
    }
  }, []);

  const isNumeric = (value) => /^-?\d*\.?\d+$/.test(value);

  const hasInvalidFields = () => {
    if (!numVariables || !numEquations || (problemType === "goal" && !numGoals)) return true;
    if (problemType === "normal") {
    if (objectiveCoefficients.length !== numVariables || objectiveCoefficients.some(v => v === "" || !isNumeric(v))) return true;
    }
    for (let constraint of constraints) {
      if (!constraint || constraint.coefficients.length !== numVariables ||
        constraint.coefficients.some(v => v === "" || !isNumeric(v)) ||
        constraint.rhs === "" || !isNumeric(constraint.rhs)) return true;
    }

    if (problemType === "goal") {
      for (let goal of goals) {
        if (!goal || goal.coefficients.length !== numVariables ||
          goal.coefficients.some(v => v === "" || !isNumeric(v)) ||
          goal.rhs === "" || !isNumeric(goal.rhs)) return true;
      }
      if (goalPriorities.length !== numGoals || goalPriorities.some(v => v === undefined || v === "" || isNaN(v))) return true;
    }
    return false;
  };

  const sendDataToServer = async () => {
    if (hasInvalidFields()) {
      alert("Please ensure all fields are filled in with valid numbers.");
      return;
    }

    const requestData = {
      problemType,
      objectiveCoefficients,
      objectiveType,
      technique,
      constraints,
      goals,
      unrestrictedVariables,
      goalPriorities
    };

    try {
      setIsLoading(true);
      const response = await fetch("http://127.0.0.1:5000/process-data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
        
      });
      console.log(requestData);
      console.log(response);

      if (!response.ok) throw new Error("Failed to send data");

      const responseData = await response.json();
      localStorage.setItem("linearProgrammingState", JSON.stringify({
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
        goalPriorities
      }));

      setTimeout(() => {
        setIsLoading(false);
        navigate("/simplex-result", {
          state: {
            status: responseData.status,
            optimalValue: responseData.optimalZ,
            xValues: responseData.xValues,
            tableaux: responseData.tableau,
            problemType
          }
        });
      }, 1500);
    } catch (error) {
      console.error("Error sending data:", error);
    }
  };

  const handleReload = () => {
    localStorage.clear();
    window.location.reload();
  };

  return (
    <div style={{ padding: "20px", margin: "auto", textAlign: "center" }}>
      <h1>Linear Programming Solver</h1>

      <ProblemFormSelector
        problemType={problemType}
        setProblemType={setProblemType}
        technique={technique}
        setTechnique={setTechnique}
        numVariables={numVariables}
        setNumVariables={setNumVariables}
        numEquations={numEquations}
        setNumEquations={setNumEquations}
        numGoals={numGoals}
        setNumGoals={setNumGoals}
      />

      {problemType === "normal" && (
        <ObjectiveFunction
          numVariables={numVariables}
          objectiveType={objectiveType}
          setObjectiveType={setObjectiveType}
          objectiveCoefficients={objectiveCoefficients}
          setObjectiveCoefficients={setObjectiveCoefficients}
        />
      )}

      <ConstraintsInput
        title="Constraints"
        numRows={numEquations}
        numVariables={numVariables}
        values={constraints}
        setValues={setConstraints}
      />

      {problemType === "goal" && (
        <GoalProgrammingSection
          numGoals={numGoals}
          numVariables={numVariables}
          goals={goals}
          setGoals={setGoals}
          goalPriorities={goalPriorities}
          setGoalPriorities={setGoalPriorities}
        />
      )}

      {numVariables > 0 && (
        <UnrestrictedVariables
          numVariables={numVariables}
          unrestrictedVariables={unrestrictedVariables}
          setUnrestrictedVariables={setUnrestrictedVariables}
        />
      )}

      <button onClick={sendDataToServer} style={{ width: "100%", marginTop: "10px", padding: "10px", backgroundColor: "#93c5fd", color: "black", border: "none", cursor: "pointer" }}>Solve</button>
      <button onClick={handleReload} style={{ width: "100%", marginTop: "10px", padding: "10px", backgroundColor: "white", color: "black", border: "none", cursor: "pointer" }}>Clear Inputs</button>

      {isLoading && (
        <div className="loading-overlay">
          <div className="loader"></div>
          <p>Hang tight! We're almost there...</p>
        </div>
      )}
    </div>
  );
};

export default LinearProgrammingSolver;