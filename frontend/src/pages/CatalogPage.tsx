import React, {useEffect, useState} from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'

interface Category {
  id: number
  name: string
  children: Category[]
  documents: any[]
}

export default function CatalogPage(){
  const [cats, setCats] = useState<Category[]>([])

  useEffect(()=>{
    axios.get('/api/catalog/').then(r => setCats(r.data)).catch(console.error)
  },[])

  return (
    <div style={{padding:20}}>
      <h1>Каталог</h1>
      {cats.map(c => (
        <div key={c.id} style={{marginBottom:10}}>
          <h3>{c.name}</h3>
          {c.documents && c.documents.map((d:any)=>(<div key={d.id}><Link to={'/document/'+d.id}>{d.title}</Link></div>))}
          {c.children && c.children.map(ch=>(<div key={ch.id} style={{marginLeft:20}}>{ch.name}</div>))}
        </div>
      ))}
    </div>
  )
}
