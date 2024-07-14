![img.png](img.png)

# ScrapMechanic logic tools

## Examples

```py
import block_list # list of blocks and objects
import color_list # list of blocks and objects
import sm_helpers as sm
import CPU_Components as cc

blocks = block_list.blocks()  # list of usable blocks
objects = block_list.objects()  # list of usable objects
colors = color_list.colors()  # list of Scrap Mechanic Colors

ID = sm.ID()  # init ID class
blueprint = sm.Blueprint(ID)  # init Blueprint class

```