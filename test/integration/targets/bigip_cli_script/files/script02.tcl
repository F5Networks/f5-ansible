proc script::init {} {
    set ::obj_count 0
   set ::match_count 0
   set ::match_info ""
   set ::usage "<pattern> <list command args...>"
}

proc check_for_match { id cur_setting cur_result_var } {

    upvar $cur_result_var cur_result

    if { [regexp $::pattern $cur_setting] == 1 } {
       append cur_result "    $id: $cur_setting\n"
       incr ::match_count
       return 1
   } else {
       return 0
    }
}

proc search_object { obj_var name_var } {

    upvar $obj_var obj
   upvar $name_var name

    incr ::obj_count
   set match 0
   set cur_result ""

    # search the oid
   if { [check_for_match "Object Identifier" [tmsh::get_name $obj] cur_result] } {
       set match 1
       # don't place the object ID in results, it will be displayed below
       set cur_result ""
    }

    # search property settings
   foreach fld [tmsh::get_field_names value $obj] {
       if { [tmsh::get_field_value $obj $fld cur_setting] } {
           if { [check_for_match $fld $cur_setting cur_result] } {
               set match 1
           }
       }
    }

    # search nested objects (pool members, ...)
   foreach fld [tmsh::get_field_names nested $obj] {
       foreach nested_obj [tmsh::get_field_value $obj $fld] {
           set nested_name "$name $fld [tmsh::get_name $nested_obj]"
           search_object nested_obj nested_name
       }
    }

    # put all matches for the current object in a single block
   if {$match} {
       append ::match_info "[tmsh::get_type $obj] : $name\n"
       append ::match_info $cur_result
    }
}

proc script::run {} {

    # the pattern is required, the component is optional, if the component is
   # not specified, then the script will run operate on the config that is
   # in the command mode where the script was issued
   if { $tmsh::argc < 2 } {
       puts $::usage
       exit 0
    }

    set ::pattern [lindex $tmsh::argv 1]

    set component ""
   if { $tmsh::argc > 2 } {
       set component [lrange $tmsh::argv 2 end]
    }

    # retrieve the set of objects to search
   if { [catch { set objs [tmsh::get_config $component] } err] } {
       puts $err
       exit 0
    }

    # recursively search the config
   foreach obj $objs {
       set name [tmsh::get_name $obj]
       search_object obj name
    }

    # send the results to the pager
   set result \
       "found $::match_count matches in $::obj_count configuration objects\n"
   append result $::match_info
   tmsh::display $result
}

proc script::help {} {
    if {$tmsh::argc < 2} {
       tmsh::add_help $::usage
   }
   else {
       # csh for the command module and/or component
       tmsh::builtin_help "list" [lrange $tmsh::argv 2 end]
    }
}

proc script::tabc {} {
    if {$tmsh::argc < 2} {
       tmsh::add_tabc $::usage
   }
   else {
       # tab completion for the command module and/or component
       tmsh::builtin_tabc "list" [lrange $tmsh::argv 2 end]
    }
}
