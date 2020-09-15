# This protocol serves the preparation of a Cystathionine-B-synthase (CBS) thermal denaturation assay in a standard green PCR microwell plate from BioRad (#HSP3841).
# Objective: screen small library of compounds at 30uM concentration
# it is OK to prepare assay at room temperature to include a 30 min RT incubation step before heating from 25 (RT) to 95°C

from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

def run(protocol: protocol_api.ProtocolContext):
    #######################################################################################################################################
    ## SETUP
    
    # Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    reaction_plate = temp_mod.load_labware("== custom labware definition goes here ==", label = "reaction plate") # where the magic happens
    # tube_rack = protocol.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul", "6", label = "aluminum block") # CBS and substrate stocks
    sample_plate = protocol.load_labware("greiner_96_wellplate_323ul", "6", label = "sample plate") # CBS and dye stocks (!!! protect dye from light !!!)
    library_plate = protocol.load_labware("greiner_96_wellplate_323ul", "5", label = "library plate") # compound library
    
    # Specify tip racks
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_10ul", '2')
    tiprack2 = protocol.load_labware("opentrons_96_tiprack_300ul", '3')

    # Load pipettes and set parameters
    p10 = protocol.load_instrument("p10_multi", "right", tip_racks = [tiprack1])
    p50 = protocol.load_instrument('p50_multi', "left", tip_racks = [tiprack2])

    p10.flow_rate.aspirate = 8
    p10.flow_rate.dispense = 8
    # 384-well depth is 11.56 mm and max volume is 112 uL
    # 20 uL is 2 mm high, tandem (middle) wall is 5.1 mm high
    p50.well_bottom_clearance.dispense = 7

    # Specify target wells (ONLY NEED TO EDIT WELLS HERE)
    samples = ["1", "2"] # columns on sample plate with protein and dye
    cols_compounds = [6, 7, 8, 9, 10] # library columns to aspirate compounds from
    cols_woSAM = [7, 8, 9, 10, 11] # destination wells in reaction plate (384-tandem)
    cols_wSAM = [12, 13, 14, 15, 16] # destination wells in reaction plate (384-tandem) (30 uM SAM final c)
    wells_reaction_woSAM = ['A' + str(i) for i in cols_woSAM]
    wells_reaction_wSAM = ['A' + str(i) for i in cols_wSAM]
    wells_reaction = ['A' + str(i) for i in (cols_woSAM + cols_wSAM)]
    
    #######################################################################################################################################
    ## PROCEDURE

    # Distribute 2.5 uL compound from 96-well library plate into empty well
    for i in range(0, len(cols_compounds)): # iterate through every column on the compound plate
        lib_col = str(cols_compounds[i]) # column of the library plate (single number)
        wells_target = [wells_reaction_woSAM[i], wells_reaction_wSAM[i]] # wells to distribute to (each compound is tested w/ and w/o SAM, so two apart columns)
        p10.distribute(2.5, library_plate.columns_by_name()[lib_col], [reaction_plate.wells_by_name()[j] for j in wells_target], new_tip = 'once')

    # Transfer 5uL fluorescent dye from sample plate to reaction plate
    p50.distribute(5, sample_plate.columns_by_name()[samples[0]], [reaction_plate.wells_by_name()[i] for i in wells_reaction])

    # Distribute 17.5 protein
    p50.distribute(17.5, sample_plate.columns_by_name()[samples[0]], [reaction_plate.wells_by_name()[i] for i in wells_reaction], new_tip = 'once')
    

# SAMPLE CODE
# p20.transfer(20,reservoir_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["A1"])
# p20.distribute(10,reservoir_plate.wells_by_name()["A2"],[mix_plate.wells_by_name()[well_name] for well_name in ["B1","C1","E1","G1","H1"]])
# p20.pick_up_tip()
# p20.transfer(10,mix_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["B1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["B1"],mix_plate.wells_by_name()["C1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["C1"],mix_plate.wells_by_name()["D1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["D1"],mix_plate.wells_by_name()["E1"],mix_after=(3,10),new_tip="never")
# p20.drop_tip()
# p20.transfer(20,reservoir_plate.wells_by_name()["A3"],mix_plate.wells_by_name()["F1"])
# p20.pick_up_tip()
# p20.transfer(10,mix_plate.wells_by_name()["F1"],mix_plate.wells_by_name()["G1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["G1"],mix_plate.wells_by_name()["H1"],mix_after=(3,10),new_tip="never")
# p20.drop_tip()

# p10.transfer(4,mix_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["A2"])
# p20.transfer(36,reservoir_plate.wells_by_name()["A4"],mix_plate.columns_by_name()["2"],new_tip='always')
# p10.well_bottom_clearance.dispense = 1
# rows=["A","B","C","D","E","F","G","H"]
# reaction_row_dest = "B"
# p10.transfer(10,mix_plate.columns_by_name()["2"],[reaction_plate.wells_by_name()[well_name] for well_name in ["B2","B3","B4"]])
# # for row in rows:
# # 	p20.distribute(10,mix_plate.wells_by_name()[(row+"2")],[reaction_plate.wells_by_name()[well_name] for well_name in [chr(ord(row)+1)+"2",chr(ord(row)+1)+"3",chr(ord(row)+1)+"4"]])
# p20.transfer(10,reservoir_plate.wells_by_name()["A4"],[reaction_plate.wells_by_name()[well_name] for well_name in ["J2","J3","J4"]])