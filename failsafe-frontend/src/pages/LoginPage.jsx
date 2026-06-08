import { useState } from 'react'
import axios from 'axios'

function LoginPage({ onLogin }) {
  const [isSignup, setIsSignup] = useState(false)
  const [form, setForm] = useState({
    email: '',
    password: '',
    name: '',
    role: 'faculty'
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const API_URL = 'https://failsafe-api-wvs6.onrender.com/auth'

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      if (isSignup) {
        await axios.post(`${API_URL}/signup`, form)
        setIsSignup(false)
        alert('Account created! Please login.')
      } else {
        const response = await axios.post(`${API_URL}/login`, {
          email: form.email,
          password: form.password
        })
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        onLogin(response.data.user)
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>🛡️ FAILSAFE</h1>
        <p style={styles.subtitle}>
          {isSignup ? 'Create Account' : 'Faculty Login'}
        </p>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          {isSignup && (
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={form.name}
              onChange={handleChange}
              style={styles.input}
              required
            />
          )}
          
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            style={styles.input}
            required
          />
          
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            style={styles.input}
            required
          />

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'Please wait...' : isSignup ? 'Sign Up' : 'Login'}
          </button>
        </form>

        <p style={styles.toggle} onClick={() => setIsSignup(!isSignup)}>
          {isSignup ? 'Already have an account? Login' : "Don't have an account? Sign Up"}
        </p>
      </div>
    </div>
  )
}

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#f5f6fa',
    fontFamily: 'Arial, sans-serif'
  },
  card: {
    backgroundColor: 'white',
    padding: '40px',
    borderRadius: '10px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
    width: '400px',
    textAlign: 'center'
  },
  title: {
    color: '#2c3e50',
    fontSize: '36px',
    marginBottom: '5px'
  },
  subtitle: {
    color: '#7f8c8d',
    fontSize: '16px',
    marginBottom: '25px'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px'
  },
  input: {
    padding: '12px',
    fontSize: '16px',
    border: '1px solid #ddd',
    borderRadius: '5px',
    outline: 'none'
  },
  button: {
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    padding: '12px',
    fontSize: '18px',
    borderRadius: '5px',
    cursor: 'pointer',
    marginTop: '10px'
  },
  toggle: {
    color: '#3498db',
    cursor: 'pointer',
    marginTop: '20px',
    fontSize: '14px'
  },
  error: {
    backgroundColor: '#fde8e8',
    color: '#e74c3c',
    padding: '10px',
    borderRadius: '5px',
    marginBottom: '15px',
    fontSize: '14px'
  }
}

export default LoginPage