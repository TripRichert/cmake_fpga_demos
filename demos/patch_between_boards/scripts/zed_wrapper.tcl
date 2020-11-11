set_property board_part em.avnet.com:zed:part0:1.4 [current_project]
set_property "part" "XC7Z020-1CLG484" [current_project]

source [diction::getDef bdscript {*}$argv]

set_property "part" "$partname" [current_project]

if {[diction::checkForKeyPair boardname {*}$argv]} {
    set_property "board_part" "[diction::getDef boardname {*}$argv]" [current_project]
} else {
    set_property "board_part" {} [current_project]
}

upgrade_ip [get_ips  system_processing_system7_0_0] -log ip_upgrade.log

export_ip_user_files -of_objects [get_ips ] -no_script -sync -force -quiet
generate_target all [get_files  *.bd]

create_ip_run [get_files -of_objects [get_fileset sources_1] *.bd]
