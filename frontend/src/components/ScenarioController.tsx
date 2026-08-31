import { useState } from 'react'

export default function ScenarioController() {
  const [scenario, setScenario] = useState('pedestrian_crossing')
  const [status, setStatus] = useState('IDLE')

  const handleRun = async () => {
    setStatus('STARTING...')
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/scenarios/${scenario}/run`, {
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
    <div className="flex flex-col gap-1.5">
      <div className="flex items-center justify-between border-b border-slate-700/60 pb-1">
        <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-blue-500"></span>
          Simulator Control
        </h3>
        <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded border border-slate-700">WEBOTS SYNC</span>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 items-end">
        <div className="flex flex-col gap-0.5">
          <label className="text-[10px] text-slate-400 uppercase font-semibold">Scenario</label>
          <select 
            className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
          >
            <option value="pedestrian_crossing">Pedestrian Crossing</option>
            <option value="red_light">Red Light Violation</option>
            <option value="congestion">Traffic Congestion</option>
            <option value="pothole">Pothole Detection</option>
          </select>
        </div>

        <div className="flex flex-col gap-0.5">
          <label className="text-[10px] text-slate-400 uppercase font-semibold">Traffic Density</label>
          <select className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs text-slate-200 focus:outline-none focus:border-blue-500">
            <option>Low (30 Veh)</option>
            <option>Medium (60 Veh)</option>
            <option>High (90 Veh)</option>
          </select>
        </div>

        <button 
          onClick={handleRun}
          disabled={status !== 'IDLE'}
          className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-1 px-3 rounded text-xs transition-all shadow-md hover:shadow-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed uppercase tracking-wider"
        >
          {status === 'IDLE' ? '▶ Trigger Event' : status}
        </button>
      </div>
    </div>
  )
}

