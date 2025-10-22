hydro = struct();

hydro = readNEMOH(hydro,'../AOE_OBAS_v2/');
% hydro = readWAMIT(hydro,'../../WAMIT/RM3/rm3.out',[]);
% hydro = combineBEM(hydro); % Compare WAMIT
hydro = radiationIRF(hydro,60,[],[],[],1.9);
hydro = radiationIRFSS(hydro,[],[]);
hydro = excitationIRF(hydro,157,[],[],[],1.9);
writeBEMIOH5(hydro)
plotBEMIO(hydro)

