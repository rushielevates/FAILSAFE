import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = {
  'SAFE': '#27ae60',
  'AT-RISK': '#e74c3c'
}

function RiskPieChart({ summary }) {
  const data = [
    { name: 'SAFE', value: summary.total_students - summary.at_risk_count },
    { name: 'AT-RISK', value: summary.at_risk_count }
  ]

  return (
    <div style={{
      backgroundColor: 'white',
      padding: '25px',
      borderRadius: '10px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      minHeight: '350px'
    }}>
      <h3 style={{ marginBottom: '20px', color: '#2c3e50', fontSize: '16px', textAlign: 'center' }}>
        📊 Risk Distribution
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={80}
            paddingAngle={5}
            dataKey="value"
            labelLine={true}
            label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}
          >
            {data.map((entry, index) => (
              <Cell key={index} fill={COLORS[entry.name]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend verticalAlign="bottom" height={36} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

function RiskBarChart({ students }) {
  const riskRanges = [
    { range: '0-20%', count: 0 },
    { range: '20-40%', count: 0 },
    { range: '40-60%', count: 0 },
    { range: '60-80%', count: 0 },
    { range: '80-100%', count: 0 }
  ]

  students.forEach(student => {
    const risk = student.risk_probability
    if (risk <= 20) riskRanges[0].count++
    else if (risk <= 40) riskRanges[1].count++
    else if (risk <= 60) riskRanges[2].count++
    else if (risk <= 80) riskRanges[3].count++
    else riskRanges[4].count++
  })

  return (
    <div style={{
      backgroundColor: 'white',
      padding: '25px',
      borderRadius: '10px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      minHeight: '350px'
    }}>
      <h3 style={{ marginBottom: '20px', color: '#2c3e50', fontSize: '16px', textAlign: 'center' }}>
        📈 Risk Score Distribution
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={riskRanges}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="range" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#3498db" name="Students" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

function RiskCharts({ results }) {
  if (!results || !results.summary) return null

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '20px',
      marginBottom: '30px'
    }}>
      <RiskPieChart summary={results.summary} />
      <RiskBarChart students={results.students} />
    </div>
  )
}

export default RiskCharts