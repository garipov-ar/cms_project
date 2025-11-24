import React, {useEffect, useState} from 'react'
import axios from 'axios'
import { useParams } from 'react-router-dom'

export default function DocumentPage(){
  const {id} = useParams()
  const [doc, setDoc] = useState<any>(null)

  useEffect(()=>{
    axios.get('/api/documents/'+id+'/').then(r=>setDoc(r.data)).catch(console.error)
  },[id])

  if(!doc) return <div>Loading...</div>

  return (
    <div style={{padding:20}}>
      <h1>{doc.title}</h1>
      <p>Version: {doc.version}</p>
      <p>Author: {doc.author}</p>
      <a href={doc.file} target="_blank" rel="noreferrer">Скачать</a>
    </div>
  )
}
