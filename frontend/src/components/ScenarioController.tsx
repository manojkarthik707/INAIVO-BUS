import { useState } from 'react'

export default function ScenarioController() {
  const [scenario, setScenario] = useState('pedestrian_crossing')
  const [status, setStatus] = useState('IDLE')

  const handleRun = async () => {
    setStatus('STARTING...')
    try {
      const res = await fetch(`http://localhost:8000/api/scenarios/${scenario}/run`, {
        method: 'POST'
      })
      if (res.ok) {
        setStatus('RUNNING')
        setTimeout(() => setStatus('IDLE'), 3000)
      } else {
        setStatus('ERROR')
      }
    } catch (e) {
      console.error(e)
      setStatus('ERROR')
    }
  }

  return (
    <div className="flex flex-col gap-3 min-w-[250px]">
      <h3 className="text-lg font-bold border-b border-slate-700 pb-2">Simulator Control</h3>
      
      <div className="flex flex-col gap-1">
        <label className="text-xs text-slate-400 uppercase font-semibold">Scenario</label>
        <select 
          className="bg-slate-800 border border-slate-600 rounded p-2 text-sm focus:outline-none focus:border-blue-500"
          value={scenario}
          onChange={(e) => setScenario(e.target.value)}
        >
          <option value="pedestrian_crossing">Pedestrian Crossing</option>
          <option value="red_light">Red Light Violation</option>
          <option value="congestion">Traffic Congestion</option>
          <option value="pothole">Pothole Detection</option>
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-xs text-slate-400 uppercase font-semibold">Traffic Density</label>
        <select className="bg-slate-800 border border-slate-600 rounded p-2 text-sm focus:outline-none focus:border-blue-500">
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>
      </div>

      <button 
        onClick={handleRun}
        disabled={status !== 'IDLE'}
        className="mt-2 w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {status === 'IDLE' ? 'RUN SCENARIO' : status}
      </button>
    </div>
  )
}
