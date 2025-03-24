import React from 'react';


const Tableau = ({ tableau }) => {
  return (
    <div className="tableau-container">
      {tableau.note && <h3 className="tableau-note">{tableau.note}</h3>}
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
  );
};

export default Tableau;
