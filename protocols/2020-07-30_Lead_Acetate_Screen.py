# This protocol serves the preparation of a Cystathionine-B-synthase (CBS) activity assay in a microwell plate from Corning (3701).
# The 384-well microplate was customized by CNC machine milling (Leo) to form a tandem of two vertically adjacent wells.

from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

# the '+ str(1)' term adds column number
well_names = [chr(ord('A') + i) + str(1) for i in range (0, 16, 2)]

def run(protocol: protocol_api.ProtocolContext):
    ## SETUP
    # Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    tube_rack = protocol.load_labware("opentrons_24_aluminumblock_nest_1.5ml_snapcap", "4", label = "aluminum block")
    reservoir_plate = protocol.load_labware("usascientific_12_reservoir_22ml", "6", label = 'reseroir plate')
    reaction_plate = temp_mod.load_labware("corning_384_wellplate_112ul_flat", label = "reaction plate")
    
    # Specify tip racks
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_10ul", '1')
    tiprack2 = protocol.load_labware("opentrons_96_tiprack_300ul", '2')
    
    # Load pipettes
    p20 = protocol.load_instrument("p20_single_gen2", "right", tip_racks = [tiprack1])
    p50 = protocol.load_instrument('p50_multi', "left", tip_racks = [tiprack2])
    p20.flow_rate.aspirate = 8
    p20.flow_rate.dispense = 8
    
    ## PROCEDURE
    # Transfer 20uL detection reagent from reservoir to reaction plate
    p50.transfer(20, reservoir_plate.columns_by_name()["1"], reaction_plate.wells_by_name()["B1", new_tip = 'once'])
    # Distribute 2uL protein from single 1.5mL tube onto odd wells starting with A1
    p20.distribute(2, tube_rack.wells()[0], [reaction_plate.wells_by_name()[well_name] for well_name in well_names], new_tip = 'once')
    # in the next protocol ater optimizing this one:
    # transfer compounds from library plate to reaction plate
    # Transfer 18 uL reaction mix to A1 of reaction plate
    p50.transfer(18, reservoir_plate.columns_by_name()["2"], reaction_plate.wells_by_name()["A1"])


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

