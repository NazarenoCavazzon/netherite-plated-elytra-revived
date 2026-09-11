package netheriteelytra;

import net.fabricmc.api.ModInitializer;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Unit;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.minecraft.world.item.equipment.Equippable;

/**
 * Netherite Plated Elytra — un elytra mejorado en la mesa de herrería.
 *
 * No depende de fabric-api a nivel de codigo: registra el item con las APIs de vanilla.
 * SI requiere fabric-api en runtime (lo aporta el pack): en 26.2 los registries se
 * congelan en Bootstrap.bootStrap(), antes de onInitialize(), y es Fabric API
 * (fabric-registry-sync-v0) quien difiere ese freeze para permitir agregar items.
 * El item es un {@link Item} común (igual que el elytra vanilla en 26.2) y saca
 * todo su comportamiento de data components:
 *   - minecraft:glider      => permite planear como un elytra.
 *   - minecraft:equippable  => se equipa en el pecho y usa nuestro modelo/equipment asset.
 *   - minecraft:damage_resistant (fireResistant) => no se quema en fuego/lava.
 *   - minecraft:attribute_modifiers => +4 de armadura en el pecho.
 *   - minecraft:max_damage  => 864 (2x los 432 del elytra vanilla).
 */
public class NetheriteElytraMod implements ModInitializer {
    public static final String ID = "netheriteelytra";
    public static final String ITEM_PATH = "netherite_plated_elytra";

    /** Clave del item en el registro (namespace propio). */
    public static final ResourceKey<Item> ITEM_KEY =
            ResourceKey.create(Registries.ITEM, Identifier.fromNamespaceAndPath(ID, ITEM_PATH));

    /** Equipment asset propio: assets/netheriteelytra/equipment/netherite_plated_elytra.json */
    public static final ResourceKey<EquipmentAsset> EQUIPMENT_ASSET =
            ResourceKey.create(EquipmentAssets.ROOT_ID, Identifier.fromNamespaceAndPath(ID, ITEM_PATH));

    public static final Item NETHERITE_PLATED_ELYTRA = new Item(new Item.Properties()
            .setId(ITEM_KEY)
            .stacksTo(1)
            .durability(864)                     // 2x el elytra vanilla (432)
            .rarity(Rarity.EPIC)
            .fireResistant()                     // no se destruye en fuego/lava
            .component(DataComponents.GLIDER, Unit.INSTANCE)
            .component(DataComponents.EQUIPPABLE, Equippable.builder(EquipmentSlot.CHEST)
                    .setEquipSound(SoundEvents.ARMOR_EQUIP_ELYTRA)
                    .setAsset(EQUIPMENT_ASSET)
                    .setDamageOnHurt(false)
                    .build())
            .repairable(Items.NETHERITE_INGOT)
            .attributes(ItemAttributeModifiers.builder()
                    .add(Attributes.ARMOR,
                            new AttributeModifier(
                                    Identifier.fromNamespaceAndPath(ID, "armor"),
                                    4.0D,
                                    AttributeModifier.Operation.ADD_VALUE),
                            EquipmentSlotGroup.CHEST)
                    .build()));

    @Override
    public void onInitialize() {
        Registry.register(BuiltInRegistries.ITEM, ITEM_KEY, NETHERITE_PLATED_ELYTRA);
    }
}
