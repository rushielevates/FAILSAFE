import { useState } from 'react'
import axios from 'axios'
import RiskCharts from '../components/RiskChart'

function Dashboard({ user, onLogout }) {
  const [file, setFile] = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const API_URL = 'https://failsafe-api-wvs6.onrender.com/api'

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setError(null)
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a CSV file first')
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post(`${API_URL}/predict`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResults(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
  <div>
    <span style={styles.welcome}>Welcome, {user.name}</span>
    <span style={styles.role}> ({user.role})</span>
  </div>
  <button onClick={onLogout} style={styles.logoutBtn}>Logout</button>
</div>
      <h1 style={styles.title}>🛡️ FAILSAFE Dashboard</h1>
      <p style={styles.subtitle}>Upload student data to identify at-risk students</p>

      {/* Upload Section */}
      <div style={styles.uploadBox}>
        <input 
          type="file" 
          accept=".csv" 
          onChange={handleFileChange}
          style={styles.fileInput}
        />
        <button 
          onClick={handleUpload} 
          disabled={loading}
          style={styles.button}
        >
          {loading ? '🔍 Analyzing...' : '📊 Predict Risk'}
        </button>
        {file && <p style={styles.fileName}>📁 {file.name}</p>}
      </div>

      {/* Error */}
      {error && <p style={styles.error}>❌ {error}</p>}

      {/* Summary */}
      {results && (
        <div style={styles.summaryBox}>
          <h2>📊 Results Summary</h2>
          <div style={styles.statsRow}>
            <div style={styles.statCard}>
              <h3>{results.summary.total_students}</h3>
              <p>Total Students</p>
            </div>
            <div style={{...styles.statCard, backgroundColor: '#ffeaa7'}}>
              <h3>{results.summary.at_risk_count}</h3>
              <p>At-Risk Students</p>
            </div>
            <div style={{...styles.statCard, backgroundColor: '#ff7675'}}>
              <h3>{results.summary.at_risk_percentage}%</h3>
              <p>Risk Percentage</p>
            </div>
          </div>
        </div>
      )}
      {/* Charts - ADD THIS */}
      {results && <RiskCharts results={results} />}
       {/* Student List */}
      {results && (
        <div style={styles.studentList}>
          <h2>👨‍🎓 Student Details</h2>
          {results.students.map((student) => (
            <div 
              key={student.student_id} 
              style={{
                ...styles.studentCard,
                borderLeft: student.prediction === 'AT-RISK' ? '5px solid #e74c3c' : '5px solid #27ae60'
              }}
            >
              <div style={styles.studentHeader}>
                <h3>Student #{student.student_id + 1}</h3>
                <span style={{
                  ...styles.badge,
                  backgroundColor: student.prediction === 'AT-RISK' ? '#e74c3c' : '#27ae60'
                }}>
                  {student.prediction === 'AT-RISK' ? '⚠️ AT-RISK' : '✅ SAFE'}
                </span>
              </div>
              <p style={styles.riskScore}>
                Risk Score: <strong>{student.risk_probability}%</strong>
              </p>
              
              {/* Risk Factors */}
               {student.risk_factors.length > 0 && (
                <div>
                  <p style={styles.factorsTitle}>Top Factors:</p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {student.risk_factors.map((factor, idx) => (
                      <span key={idx} style={{
                        ...styles.factorTag,
                        backgroundColor: factor.direction === 'risk' ? '#fde8e8' : '#e8f8e8',
                        color: factor.direction === 'risk' ? '#c0392b' : '#27ae60',
                        border: factor.direction === 'risk' ? '1px solid #f5c6cb' : '1px solid #c3e6cb'
                      }}>
                        {factor.direction === 'risk' ? '🔴' : '🟢'} {factor.feature}: {factor.impact > 0 ? '+' : ''}{factor.impact.toFixed(1)}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Intervention Plan */}
              {student.interventions && student.interventions.length > 0 && (
                <div style={{ marginTop: '15px' }}>
                  <p style={{ fontWeight: 'bold', marginBottom: '8px' }}>
                    📋 Intervention Plan:
                  </p>
                  {student.interventions.map((item, idx) => (
                    <div key={idx} style={{
                      backgroundColor: '#fff3cd',
                      padding: '10px',
                      borderRadius: '5px',
                      marginBottom: '8px',
                      borderLeft: '4px solid #f39c12'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <strong style={{ fontSize: '14px' }}>{item.action}</strong>
                        <span style={{
                          backgroundColor: item.priority === 'Critical' ? '#e74c3c' : 
                                         item.priority === 'High' ? '#e67e22' : '#3498db',
                          color: 'white',
                          padding: '2px 10px',
                          borderRadius: '10px',
                          fontSize: '11px'
                        }}>
                          {item.priority}
                        </span>
                      </div>
                      <p style={{ fontSize: '13px', color: '#666', margin: '5px 0' }}>{item.detail}</p>
                      <p style={{ fontSize: '12px', color: '#999' }}>⏰ {item.timeline}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// Styles

const styles = {
  container: {
    maxWidth: '900px',
    margin: '0 auto',
    padding: '30px',
    fontFamily: 'Arial, sans-serif'
  },
  title: {
    color: '#2c3e50',
    fontSize: '36px',
    marginBottom: '5px'
  },
  subtitle: {
    color: '#7f8c8d',
    fontSize: '18px',
    marginBottom: '30px'
  },
  uploadBox: {
    backgroundColor: '#f8f9fa',
    padding: '30px',
    borderRadius: '10px',
    textAlign: 'center',
    marginBottom: '30px'
  },
  fileInput: {
    marginBottom: '15px',
    fontSize: '16px'
  },
  button: {
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    padding: '12px 30px',
    fontSize: '18px',
    borderRadius: '5px',
    cursor: 'pointer'
  },
  fileName: {
    color: '#27ae60',
    marginTop: '10px'
  },
  error: {
    color: '#e74c3c',
    backgroundColor: '#fde8e8',
    padding: '15px',
    borderRadius: '5px',
    marginBottom: '20px'
  },
  summaryBox: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '10px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    marginBottom: '30px'
  },
  statsRow: {
    display: 'flex',
    gap: '20px',
    marginTop: '20px'
  },
  statCard: {
    flex: 1,
    backgroundColor: '#dfe6e9',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center'
  },
  studentList: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '10px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
  },
  studentCard: {
    backgroundColor: '#f8f9fa',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '15px'
  },
  studentHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px'
  },
  badge: {
    color: 'white',
    padding: '5px 15px',
    borderRadius: '20px',
    fontSize: '14px',
    fontWeight: 'bold'
  },
  riskScore: {
    fontSize: '16px',
    marginBottom: '10px'
  },
  factorsTitle: {
    fontWeight: 'bold',
    marginBottom: '5px'
  },
  factorTag: {
    display: 'inline-block',
    padding: '5px 12px',
    borderRadius: '15px',
    margin: '3px',
    fontSize: '13px'
  },
  header: {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '20px',
  padding: '15px',
  backgroundColor: 'white',
  borderRadius: '10px',
  boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
},
welcome: {
  fontWeight: 'bold',
  fontSize: '16px'
},
role: {
  color: '#7f8c8d',
  fontSize: '14px'
},
logoutBtn: {
  backgroundColor: '#e74c3c',
  color: 'white',
  border: 'none',
  padding: '8px 20px',
  borderRadius: '5px',
  cursor: 'pointer'
}
}

export default Dashboard