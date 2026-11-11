const catalog=require('../data/catalog');
const pointById=Object.create(null),routeById=Object.create(null);
catalog.points.forEach(p=>{pointById[p.id]=p;});
catalog.routes.forEach(r=>{routeById[r.id]=r;});
function list({keyword='',district='全部',metroStation='全部',maxMinutes=0,includeDrafts=false}={}){
 const q=keyword.trim().toLowerCase();
 return catalog.routes.filter(r=>(includeDrafts||r.status==='verified')&&
  (district==='全部'||r.district===district)&&(metroStation==='全部'||r.metroStation===metroStation)&&
  (!Number(maxMinutes)||r.totalMinutes<=Number(maxMinutes))&&
  (!q||[r.name,r.summary,r.district,r.metroStation,...r.tags,...r.stops.map(s=>pointById[s.pointId].name)].join(' ').toLowerCase().includes(q)));
}
function detail(id){const r=routeById[id];return r?{...r,stops:r.stops.map(s=>({...s,point:pointById[s.pointId]}))}:null;}
module.exports={catalog,list,detail,pointById};
