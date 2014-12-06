###Notes:
* Instructions first "complete" and then if they are not waiting for other instructions they 'graduate' 
* Physical registers range from 1 to 64 (there is no register 0)
* Processor decodes and **GRADUATES** 4 instructions per cycle (in parallel)

* **Logical Registers (ALU Registers): Actual registers appearing within instruction fields**
    * Physical Registers : Locations in the actual hardware register file
    * Mapping the logical level to the Physical 
    * ROB == Active list
    * a completed or an incompleted instruction that remains on the reorder buffer 
      must be aborted if it follows an exception or a mispredict branch  
    * 33 logical (1-31 plus hi and lo) and 64 physical integer registers
    * 32 logical (0-31) and 64 physical floating point registers 
    * register map table: unit that maps logical to physical registers
        - 16 read ports (4 instructions x 4 registers)
    * Integer AND FP free lists contain list of currently unassigned physical registers

* **Active List - ROB :**
 * 32 Instructions can be active so it should be having 32 spots
 * It has to remove instructions when they commit
 * It has to remove instructions if a mispredicted 
 * branch or an exception causes them to abort
* **Active List Record : Each record in the Active List contains:**
 * the logical DESTINATION register
 * the physical register
 * a bit specifying if the current

* Instruction queues
 * 3 Instruction Queues:
   * Integer queue : Branch and shift instructions have priority for ALU1 queue, multiply and divide have priority for ALU2 queue 
   * Integer queue, FP queue and Address queue contain 16 entries each


### Questions

* There is no destination register for store words what do I do as far as ROB goes?
  Should I add an entry anyway? (probably yes I need to check that!) 
  Also same question for branches.