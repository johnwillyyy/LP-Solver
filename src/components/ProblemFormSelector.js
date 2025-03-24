import React from "react";

const ProblemFormSelector = ({
  problemType,
  setProblemType,
  technique,
  setTechnique,
  numVariables,
  setNumVariables,
  numEquations,
  setNumEquations,
  numGoals,
  setNumGoals
}) => {
  return (
    <div>
      <label>Select Problem Type: </label>
      <select value={problemType} onChange={(e) => setProblemType(e.target.value)}>
        <option value="normal">Normal Min/Max Problem</option>
        <option value="goal">Goal Programming</option>
      </select>

      {problemType === "normal" && (
        <select value={technique} onChange={(e) => setTechnique(e.target.value)}>
          <option value="bigm">Big M</option>
          <option value="twophase">Two-Phase</option>
        </select>
      )}

      <div>
        <input
          type="number"
          placeholder="Number of Variables"
          value={numVariables}
          onChange={(e) => setNumVariables(Number(e.target.value))}
        />
        <input
          type="number"
          placeholder="Number of Constraints"
          value={numEquations}
          onChange={(e) => setNumEquations(Number(e.target.value))}
        />
        {problemType === "goal" && (
          <input
            type="number"
            placeholder="Number of Goals"
            value={numGoals}
            onChange={(e) => setNumGoals(Number(e.target.value))}
          />
        )}
      </div>
    </div>
  );
};

export default ProblemFormSelector;
