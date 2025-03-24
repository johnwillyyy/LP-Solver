const GoalResults = ({ optimalValue, xValues }) => {
    return (
      <>
        <div className="goal-status-box">
          <p className="solution-title">Goal Status:</p>
          <div className="goal-status-values">
            {optimalValue.map(([goalName, status], index) => (
              <div key={index} className="goal-status-item">
                <strong>{goalName}</strong>:{" "}
                <span
                  className={
                    status === "Satisfied" ? "status-satisfied" : "status-unsatisfied"
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
    );
  };
  
  export default GoalResults;
  