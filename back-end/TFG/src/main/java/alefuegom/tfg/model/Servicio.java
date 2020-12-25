package alefuegom.tfg.model;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import com.sun.istack.NotNull;

@Entity
@Table(name="servicios")
public class Servicio extends BaseEntity {
	
	@NotNull
	@Enumerated(EnumType.ORDINAL) 
	private EstadoServicio estado;
	
	private String observaciones;
	
	@ManyToOne(cascade = CascadeType.ALL)
	private Trabajador trabajador;
	
	@OneToOne(cascade = CascadeType.ALL)
	private SolicitudServicio solicitud;
	
	@OneToOne(optional=true, cascade = CascadeType.ALL)
	private Factura factura;
	
	
}
