import React from "react";
import ConstraintsInput from "./ConstraintsInput";

const GoalProgrammingSection = ({
  numGoals,
  numVariables,
  goals,
  setGoals,
  goalPriorities,
  setGoalPriorities
}) => {
  const handlePriorities = (index, value) => {
    const updated = [...goalPriorities];
    updated[index] = value;

    const parsed = updated.map(val => val ? parseInt(val) : null);
    const ranks = Array(numGoals).fill(0);

    parsed.forEach((val, inputIndex) => {
      if (val && val >= 1 && val <= numGoals) {
        ranks[val - 1] = inputIndex + 1;
      }
    });

    setGoalPriorities(ranks);
  };

  return (
    <div>
      <ConstraintsInput
        title="Goal Equations"
        numRows={numGoals}
        numVariables={numVariables}
        values={goals}
        setValues={setGoals}
      />

      <h2>Goal Prioritization</h2>
      {Array.from({ length: numGoals }).map((_, index) => (
        <React.Fragment key={index}>
          <input
            type="number"
            min="1"
            max={numGoals}
            placeholder={`Priority for Goal ${index + 1}`}
            onChange={(e) => handlePriorities(index, e.target.value)}
          />
          {index < numGoals - 1 && <span style={{ margin: "0 10px" }}>&gt;</span>}
        </React.Fragment>
      ))}
    </div>
  );
};

export default GoalProgrammingSection;
