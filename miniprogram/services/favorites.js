const KEY='citywalk:favorites:v1';
function list(){try{const ids=wx.getStorageSync(KEY);return Array.isArray(ids)?[...new Set(ids.filter(x=>typeof x==='string'&&/^gyr_[0-9]{3,6}$/.test(x)))]:[];}catch(_){return [];}}
function toggle(id){if(!/^gyr_[0-9]{3,6}$/.test(id))throw Error('无效路线ID');let ids=list();ids=ids.includes(id)?ids.filter(x=>x!==id):ids.concat(id);wx.setStorageSync(KEY,ids);return ids.includes(id);}
module.exports={list,toggle};
